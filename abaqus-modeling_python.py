#!/user/bin/python
#-*-coding:UTF-8-*- 
#����������Ϊ����ʹ������
print '�ֹܻ������⻷ʽ�ڵ㽨ģ�ű�'
print 'original:Circular-CFST.py by L	iHuaWei, adapted by Lbh'
from abaqus import *
from abaqusConstants import *
from caeModules import *
import math

logical=True
while logical:
	parameter=(
		('ģ������:','CIJ'),
		('��ֱ��(������)(mm):','219'),
		('�ֹܱں�(mm):','4.68'),
		('����(mm):','1500'),
		('����(mm):','2600'),
		('����(mm):','100'),
		('����(mm):','150'),
		('����Ե���(mm):','5.62'),
		('��������(mm):','5.62'),
		('�����̺��(mm):','20'),
		('����Եfy(N/mm):','475.4'),
		('������fy(N/mm):','467.3'),
		('�ֹ�fy(N/mm):','375.4'),
		('������fcu(N/mm):','56.0'),
		('��ѹ����(N):','850000'),
		('����λ��(mm):','100'),
		('Job Name:','CIJ-default'))
	Modelname,diameter,thickness,length,b_span,b_width,b_depth,b_tf,b_tw,flange_t,fyf,fyw,fyt,fcu,load,displacement,jobname=getInputs(fields=parameter,label='���������:',dialogTitle='Model Parameter')
	listtry=[Modelname,diameter,thickness,length,b_span,b_width,b_depth,b_tf,b_tw,flange_t,fyf,fyw,fyt,fcu,load,displacement,jobname]  #?

	if listtry==[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]:
		
		
	else:
		logical=False
		
		diameter=float(diameter)
		thickness=float(thickness)
		length=float(length)
		
		b_span=float(b_span)
		b_width=float(b_width)
		b_depth=float(b_depth)
		b_tf=float(b_tf)
		b_tw=float(b_tw)
		
		#f_D=1.1366*diameter+95  #excel��ϵķ����ߴ�
		f_D=320
		#f_Dbolt=1.1134*diameter+58.75#excel��ϵ���˨λ��
		f_Dbolt=280
		bolt_d=18
		flange_t =float(flange_t)
		
		fyf=float(fyf)
		fyw=float(fyw)
		fyt=float(fyt)
		
		fcu=float(fcu)
		load=float(load)
		displacement=float(displacement)
		myModel=mdb.Model(name=Modelname)
		
		meshsize=diameter*0.15
		
	#�������ø�ʽ
	session.journalOptions.setValues(replayGeometry=INDEX,recoverGeometry=INDEX) 
	
	session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=229.333343505859, height=140.829620361328)
	session.viewports['Viewport: 1'].makeCurrent()
	session.viewports['Viewport: 1'].maximize()	
	session.viewports['Viewport: 1'].assemblyDisplay.setValues(renderShellThickness=ON)		
	session.viewports['Viewport: 1'].assemblyDisplay.geometryOptions.setValues(datumPlanes=OFF)
	session.viewports['Viewport: 1'].assemblyDisplay.geometryOptions.setValues(datumAxes=OFF)
	
	##1 Partģ��  ���˳ߴ� �ź�����         
	#!!��part���֣�������ߵ�ģ�������Ȱ�Ҫ�õļ�����
	m = (diameter/2+70)/(2**0.5)
	c_thickness = thickness   #���ɱ��
	#1.1 Ԥ�ƽڵ�-joint
	#��һ�β�ͼ  ������
	radius_ = diameter/2 - c_thickness   #�ֹܵĺ�ȱ�¶�����
	s = myModel.ConstrainedSketch(name='__profile__', sheetSize=200.0)
	s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(radius_, 0.0))
	s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(diameter/2, 0.0))
	p = myModel.Part(name='joint', dimensionality=THREE_D, type=DEFORMABLE_BODY)
	p.BaseSolidExtrude(sketch=s, depth=b_depth/2)
	del myModel.sketches['__profile__']
	#�ڶ��β�ͼ  ����
	p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=0.0)   		    #d1[2]
	p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=b_depth/2-b_tf) #d1[3]
	p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=b_tf-b_depth/2) #d1[4]
	e, d1= p.edges, p.datums
	t = p.MakeSketchTransform(sketchPlane=d1[3], sketchUpEdge=e[0], sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 0.0, 0.0))  #���origin��ɶ��
	s1 = myModel.ConstrainedSketch(name='__profile__', sheetSize=116.67, gridSpacing=2.91, transform=t)
	s1.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(diameter/2, 0.0))
	s1.Line(point1=(m, m), point2=(m+150, b_width/2))												#line����������
	s1.Line(point1=(m+150, b_width/2), point2=(m+150, -b_width/2))
	s1.Line(point1=(m+150, -b_width/2), point2=(m, -m))
	s1.ArcByCenterEnds(center=(0,0),point1=(m, -m),  point2=(-m, -m),  direction=CLOCKWISE)
	s1.Line(point1=(-m, -m), point2=(-m-150, -b_width/2))
	s1.Line(point1=(-m-150, -b_width/2), point2=(-m-150, b_width/2))
	s1.Line(point1=(-m-150, b_width/2), point2=(-m, m))
	s1.ArcByCenterEnds(center=(-0,0),point1=(-m, m), point2=(m, m), direction=CLOCKWISE)
	#���忪��
	g = s1.geometry
	bolthole = s1.CircleByCenterPerimeter(center=(f_Dbolt/2, 0.0), point1=(f_Dbolt/2+bolt_d/2, 0.0))
	s1.rotate(centerPoint=(0.0, 0.0), angle=22.5, objectList=(g[bolthole.id], ))
	s1.radialPattern(geomList=(g[bolthole.id], ), vertexList=(), number=8, totalAngle=360.0, centerPoint=(0.0, 0.0))
	p.SolidExtrude(sketchPlane=d1[3], sketchUpEdge=e[0], sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, sketch=s1, depth=b_tf, flipExtrudeDirection=OFF)
	del myModel.sketches['__profile__']
	#�����β�ͼ  
	p.DatumAxisByPrincipalAxis(principalAxis=YAXIS) #d1[6]
	t = p.MakeSketchTransform(sketchPlane=d1[2], sketchUpEdge=d1[6], sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 0.0, 0.0))
	s = myModel.ConstrainedSketch(name='__profile__', sheetSize=1.0, gridSpacing=1.0, transform=t)
	p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
	diameter_k=0.49*diameter
	s.Line(point1=(diameter_k, b_tw/2), point2=(m+150, b_tw/2))
	s.Line(point1=(m+150, b_tw/2), point2=(m+150, -b_tw/2))
	s.Line(point1=(m+150, -b_tw/2), point2=(diameter_k, -b_tw/2))
	s.Line(point1=(diameter_k, -b_tw/2), point2=(diameter_k, b_tw/2))
	
	s.Line(point1=(-diameter_k, b_tw/2), point2=(-m-150, b_tw/2))
	s.Line(point1=(-m-150, b_tw/2), point2=(-m-150, -b_tw/2))
	s.Line(point1=(-m-150, -b_tw/2), point2=(-diameter_k, -b_tw/2))
	s.Line(point1=(-diameter_k, -b_tw/2), point2=(-diameter_k, b_tw/2))
	p.SolidExtrude(sketchPlane=d1[2], sketchUpEdge=d1[6], sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, sketch=s, depth=b_depth/2-b_tf, flipExtrudeDirection=OFF)
	del myModel.sketches['__profile__']
	#����ָ��
	p.Mirror(mirrorPlane=d1[2], keepOriginal=ON)
	#�ָ�
	p = myModel.parts['joint']
	d = p.datums
	pickedCells = p.cells[0:1]
	p.PartitionCellByDatumPlane(datumPlane=d[3], cells=pickedCells)
	pickedCells = p.cells[1:2]
	p.PartitionCellByDatumPlane(datumPlane=d[4], cells=pickedCells)
	c = p.cells
	pickedCells = c[0:1]
	p.PartitionCellByExtendFace(extendFace=p.faces[30], cells=pickedCells)
	#1.1' joint set
	#���涨�����õ���  �ڵ�ֲİ�������һ���ģ� ��ȿ�����Ӧ ��������û��Ҫ��
	c = p.cells
	p.Set(cells=c[3:5], name='huanban')
	p.Set(cells=c[2:3], name='joint-tube')
	p.Set(cells=c[0:2], name='joint-fuban')
	s = p.faces
	p.Surface(side1Faces = s[7:8]+s[12:13]+s[40:41], name='joint I y+')  #����tie
	p.Surface(side1Faces = s[8:9]+s[11:12]+s[44:45], name='joint I y-')	 #����tie
	s = p.faces   #�õ��໥�������
	p.Surface(side1Faces=s[9:10]+s[13:14]+s[55:56], name='joint-tube-inner')   #�������
	p.Surface(side1Faces=s[56:57], name='huanban-uu')   
	p.Surface(side1Faces=s[37:39], name='huanban-ud')   
	p.Surface(side1Faces=s[14:16], name='huanban-du')  
	p.Surface(side1Faces=s[30:31], name='huanban-dd')  
	#hole
	p.Surface(side1Faces=s[47:48], name='hole_joint-shang-1')
	p.Surface(side1Faces=s[54:55], name='hole_joint-shang-2')
	p.Surface(side1Faces=s[53:54], name='hole_joint-shang-3')
	p.Surface(side1Faces=s[52:53], name='hole_joint-shang-4')
	p.Surface(side1Faces=s[51:52], name='hole_joint-shang-5')
	p.Surface(side1Faces=s[50:51], name='hole_joint-shang-6')
	p.Surface(side1Faces=s[49:50], name='hole_joint-shang-7')
	p.Surface(side1Faces=s[48:49], name='hole_joint-shang-8')
	
	p.Surface(side1Faces=s[22:23], name='hole_joint-xia-1')
	p.Surface(side1Faces=s[29:30], name='hole_joint-xia-2')
	p.Surface(side1Faces=s[28:29], name='hole_joint-xia-3')
	p.Surface(side1Faces=s[27:28], name='hole_joint-xia-4')
	p.Surface(side1Faces=s[26:27], name='hole_joint-xia-5')
	p.Surface(side1Faces=s[25:26], name='hole_joint-xia-6')
	p.Surface(side1Faces=s[24:25], name='hole_joint-xia-7')
	p.Surface(side1Faces=s[23:24], name='hole_joint-xia-8')

	#1.2.1 ����
	p = myModel.Part(name='beam', dimensionality=THREE_D, type=DEFORMABLE_BODY)
	p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=m+150)
	p.DatumAxisByPrincipalAxis(principalAxis=ZAXIS)
	p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=b_depth/2-b_tf) #d[3]
	p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=b_tf-b_depth/2) #d[4]
	p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=(b_span/2-(m+150))/2+(m+150)) #d[5]   for mesh
	d1=p.datums
	t = p.MakeSketchTransform(sketchPlane=d1[1], sketchUpEdge=d1[2],
    	sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 289.5, 0.0))
	s = myModel.ConstrainedSketch(name='__profile__', sheetSize=1046.3, gridSpacing=26.15, transform=t)
	s.Line(point1=(-b_width/2, b_depth/2), point2=(b_width/2, b_depth/2))
	s.Line(point1=(b_width/2, b_depth/2), point2=(b_width/2, b_depth/2-b_tf))
	s.Line(point1=(b_width/2, b_depth/2-b_tf), point2=(b_tw/2, b_depth/2-b_tf))
	s.Line(point1=(b_tw/2, b_depth/2-b_tf), point2=(b_tw/2, -b_depth/2+b_tf))
	s.Line(point1=(b_tw/2, -b_depth/2+b_tf), point2=(b_width/2, -b_depth/2+b_tf))
	s.Line(point1=(b_width/2, -b_depth/2+b_tf), point2=(b_width/2, -b_depth/2))
	s.Line(point1=(b_width/2, -b_depth/2), point2=(-b_width/2, -b_depth/2))
	s.Line(point1=(-b_width/2, -b_depth/2), point2=(-b_width/2, b_tf-b_depth/2))
	s.Line(point1=(-b_width/2, b_tf-b_depth/2), point2=(-b_tw/2, b_tf-b_depth/2))
	s.Line(point1=(-b_tw/2, b_tf-b_depth/2), point2=(-b_tw/2, b_depth/2-b_tf))
	s.Line(point1=(-b_tw/2, b_depth/2-b_tf), point2=(-b_width/2, b_depth/2-b_tf))
	s.Line(point1=(-b_width/2, b_depth/2-b_tf), point2=(-b_width/2, b_depth/2))
	p.SolidExtrude(sketchPlane=d1[1], sketchUpEdge=d1[2], sketchPlaneSide=SIDE1, 
    	sketchOrientation=RIGHT, sketch=s, depth=b_span/2-(m+150), flipExtrudeDirection=OFF)
	del myModel.sketches['__profile__']
	#���
	p = myModel.parts['beam']
	d = p.datums
	pickedCells = p.cells[0:1]
	p.PartitionCellByDatumPlane(datumPlane=d[3], cells=pickedCells)
	pickedCells = p.cells[0:1]
	p.PartitionCellByDatumPlane(datumPlane=d[4], cells=pickedCells)
	pickedCells = p.cells[0:3]
	p.PartitionCellByDatumPlane(datumPlane=d[5], cells=pickedCells)
	#1.2.1' surface,used to tie
	s = p.faces
	p.Surface(side1Faces=s[19:20]+s[22:23]+s[36:37], name='beam-inner')
	p.Surface(side1Faces=s[18:19]+s[21:22]+s[35:36], name='beam-outer') 
	#���渳��
	c = p.cells
	p.Set(cells=c[2:4], name='web')
	p.Set(cells=c[0:2]+c[4:6], name='flange')
	
#1.3.1���¸ֹܣ����Ƕ�֧����    �˴���ģ�����趨Ϊ��ʵ�����в��죬Ϊ��ʹ����֮������С��̫����tie��������  ��ģʱ���ӷ����ĺ��    2*flange_t  �Լ�����flangeװ��Ĳ���
	p = myModel.Part(name='tube', dimensionality=THREE_D, type=DEFORMABLE_BODY)
	p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=b_depth/2)
	p.DatumAxisByPrincipalAxis(principalAxis=XAXIS)
	p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=b_depth/2+flange_t)
	d = p.datums
	t = p.MakeSketchTransform(sketchPlane=d[1], sketchUpEdge=d[2],
    	sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 0.0, 0.0))
	s = myModel.ConstrainedSketch(name='__profile__', sheetSize=1046.3, gridSpacing=26.15, transform=t)
	s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.0, radius_))        #����
	s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.0, diameter/2)) 
	p.SolidExtrude(sketchPlane=d[1], sketchUpEdge=d[2], sketchPlaneSide=SIDE1, 
    	sketchOrientation=RIGHT, sketch=s, depth=length/2-b_depth/2, flipExtrudeDirection=OFF)
	del myModel.sketches['__profile__']
	pickedCells = p.cells[0:1]
	p.PartitionCellByDatumPlane(datumPlane=d[3], cells=pickedCells)
	s = p.faces 
	p.Surface(side1Faces=s[2:3]+s[4:5], name='tube-inner')
	p.Surface(side1Faces=s[5:6], name='tube-rigid')
	p.Surface(side1Faces=s[1:2], name='tube-flange')
	p.Set(cells=p.cells[0:2], name='tube')
	
#1.3.2���¸ֹܵĽ½Ӷ�֧��
	p = myModel.Part(name='tube rigid', dimensionality=THREE_D, type=DEFORMABLE_BODY)
	p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=length/2)
	p.DatumAxisByPrincipalAxis(principalAxis=XAXIS)
	d1=p.datums
	t = p.MakeSketchTransform(sketchPlane=d1[1], sketchUpEdge=d1[2], sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 0.0, 0.0))
	s = myModel.ConstrainedSketch(name='__profile__', sheetSize=1046.3, gridSpacing=26.15, transform=t)
	g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
	s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.0, diameter/2))
	p.SolidExtrude(sketchPlane=d1[1], sketchUpEdge=d1[2], sketchPlaneSide=SIDE1, 
    	sketchOrientation=RIGHT, sketch=s, depth=length/20, flipExtrudeDirection=OFF)
	del myModel.sketches['__profile__']
	p.ConvertToAnalytical()
	p.Surface(side1Faces=p.faces[2:3], name='bottom')
	
#1.4 ���Ļ�����
	s = myModel.ConstrainedSketch(name='__profile__', sheetSize=200.0)
	s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(radius_, 0.0))
	p = myModel.Part(name='concrete', dimensionality=THREE_D, type=DEFORMABLE_BODY)
	p.BaseSolidExtrude(sketch=s, depth=length/2)
	del myModel.sketches['__profile__']
	p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=0.0)   		       #d1[2]
	p.Mirror(mirrorPlane=d1[2], keepOriginal=ON)

	#�õ��������
	p.Set(cells=p.cells[0:1], name='concrete')
	s = p.faces   #������Ϊ����
	p.Surface(side2Faces=s[1:2], name='surface-all')
	p.Surface(side2Faces=s[2:3], name='top')
	p.Surface(side1Faces=s[0:1], name='bottom')
	
#1.5 ʵ�巨���� p.BaseShell(sketch=s)
	s = myModel.ConstrainedSketch(name='__profile__', sheetSize=200.0)	
	s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(diameter/2, 0.0))
	s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.5*f_D, 0))
	#����
	g = s.geometry
	bolthole = s.CircleByCenterPerimeter(center=(f_Dbolt/2, 0.0), point1=(f_Dbolt/2+bolt_d/2, 0.0))
	s.rotate(centerPoint=(0.0, 0.0), angle=22.5, objectList=(g[bolthole.id], ))
	s.radialPattern(geomList=(g[bolthole.id], ), vertexList=(), number=8, totalAngle=360.0, centerPoint=(0.0, 0.0))
	
	p = myModel.Part(name='flange', dimensionality=THREE_D, type=DEFORMABLE_BODY)
	p.BaseSolidExtrude(sketch=s, depth=flange_t)
	del myModel.sketches['__profile__']
#1.5' ʵ�巨����set
	s = p.faces
	p.Surface(side1Faces=s[8:9], name='flange-inner')
	p.Surface(side1Faces=s[10:11], name='flange-Zouter')
	p.Surface(side1Faces=s[11:12], name='f-f')

	
	#hole
	p.Surface(side1Faces=s[7:8], name='hole_flange-1')
	p.Surface(side1Faces=s[6:7], name='hole_flange-2')
	p.Surface(side1Faces=s[5:6], name='hole_flange-3')
	p.Surface(side1Faces=s[4:5], name='hole_flange-4')
	p.Surface(side1Faces=s[3:4], name='hole_flange-5')
	p.Surface(side1Faces=s[2:3], name='hole_flange-6')
	p.Surface(side1Faces=s[1:2], name='hole_flange-7')
	p.Surface(side1Faces=s[9:10], name='hole_flange-8')
	
#1.6 ��˨���ݸ�+��ñ��     ���� Ϊʲô��
	p = myModel.Part(name='bolt', dimensionality=THREE_D, type=DEFORMABLE_BODY)
	d=p.datums
	p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=(flange_t+b_tf)/2)
	p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=0.0)
	p.DatumAxisByPrincipalAxis(principalAxis=YAXIS)
	p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=-(flange_t+b_tf)/2)
	p.DatumPlaneByOffset(plane=d[4], flip=SIDE1, offset=b_tf)
	t = p.MakeSketchTransform(sketchPlane=d[1], sketchUpEdge=d[3], sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 0.0, 0.0))      #originԭ���������˼
	s = myModel.ConstrainedSketch(name='__profile__', sheetSize=2641.93, gridSpacing=66.04, transform=t)
	s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(bolt_d/2, 0))
	p.SolidExtrude(sketchPlane=d[1], sketchUpEdge=d[3], sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, sketch=s, depth=(flange_t+b_tf)/2, flipExtrudeDirection=ON)
	del myModel.sketches['__profile__']
	#����
	R=12
	t = p.MakeSketchTransform(sketchPlane=d[1], sketchUpEdge=d[3], sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 0.0, 0.0))
	s = myModel.ConstrainedSketch(name='__profile__', sheetSize=1.0, gridSpacing=1.0, transform=t)
	s.Line(point1=(R, 0), point2=(R/2, -R/2*(3**0.5)))
	s.Line(point1=(R/2, -R/2*(3**0.5)), point2=(-R/2, -R/2*(3**0.5)))
	s.Line(point1=(-R/2, -R/2*(3**0.5)), point2=(-R, 0))
	s.Line(point1=(-R, 0), point2=(-R/2, R/2*(3**0.5)))
	s.Line(point1=(-R/2, R/2*(3**0.5)), point2=(R/2, R/2*(3**0.5)))
	s.Line(point1=(R/2, R/2*(3**0.5)), point2=(R, 0))
	p.SolidExtrude(sketchPlane=d[1], sketchUpEdge=d[3], sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, sketch=s, depth=10, flipExtrudeDirection=OFF)
	del myModel.sketches['__profile__']
	#����ָ��
	p.Mirror(mirrorPlane=d[2], keepOriginal=ON)
#1.6.1���
	p = myModel.parts['bolt']
	pickedCells = p.cells[0:1]
	d = p.datums
	p.PartitionCellByDatumPlane(datumPlane=d[1], cells=pickedCells)
	pickedCells = p.cells[1:2]
	p.PartitionCellByDatumPlane(datumPlane=d[4], cells=pickedCells)
	pickedCells = p.cells[0:1]
	p.PartitionCellByDatumPlane(datumPlane=d[5], cells=pickedCells)
#1.6' ��˨���ݸ�+��ñ��  
	s = p.faces
	p.Surface(side1Faces=s[12:13], name='bolt-b_flange')
	p.Surface(side1Faces=s[1:2]+s[20:21], name='bolt-hole')
	p.Surface(side1Faces=s[4:5], name='bolt-joint_flange')
#2 Property    ����������ֹܻ���������Ӧ��Ӧ��������   �����fcu ʵΪfcuk �����忹ѹǿ�ȱ�׼ֵ
#2.1���  E�ܴ�
	myModel.Material(name='Material-rigid')
	myModel.materials['Material-rigid'].Density(table=((7.8e-09,),))
	myModel.materials['Material-rigid'].Elastic(table=((1000000000000.0, 1e-06),))
	
	
	##��������
	fy=fyt
	########alpha1��alpha2���ж�   ���� ������ 4������ǿ�ȵ�ת��   fcuk ���ǳ�����CXX��XX������Ҫת��Ϊfck�����Ŀ�ѹǿ�ȱ�׼ֵ����fc����Բ���忹ѹǿ�ȣ���  �ÿ�������  ��Ҫ����������ǣ�
	if fcu<=50:
		alpha1=0.76
	elif fcu>=80:
		alpha1=0.82
	else:
		alpha1=0.76 + 0.002 * (fcu - 50)
	if fcu<=40:
		alpha2=1
	elif fcu>=80:
		alpha2=0.87
	else:
		alpha2 = 1 + 0.00325 * (40 - fcu)
		
	fck=0.88*alpha1*alpha2*fcu
	fc=0.79*fcu
		
	Es=206000           
	Ec=4700*sqrt(fc)    #ר��p108
	EC=float('%.2f'%Ec)
	miu=0.2             #ר��p108

	As=0.25*pi*((diameter**2)-((diameter-2*thickness)**2))
	Ac=0.25*pi*((diameter-2*thickness)**2)
	ksi=As*fy/Ac/fck         #Լ��ЧӦϵ�� ר��p28

	epsilon_e=0.8*fy/Es         #ר��P67 �ֲı�����ز���
	epsilon_e1=1.5*epsilon_e
	epsilon_e2=10*epsilon_e1
	epsilon_e3=100*epsilon_e1
	A=0.2*fy/((epsilon_e1-epsilon_e)**2)#?
	B=2*A*epsilon_e1                    #?
	C=0.8*fy+A*epsilon_e*epsilon_e-B*epsilon_e  #?
	
	#����һ���������ɺ���  ����ģ�
	
	#�ֲֹܸ�
	fy=fyt
	list1=[]
	tuple1=()
	def drange(start, stop, step):           #���巽��
		r = start 
		while r < (stop-step):
			yield r
			r+= step
	#�ֲĲ��Լ���  ���
	for epsilons in drange(epsilon_e*100000,epsilon_e1*100000,5):
		sigma=-A*epsilons*epsilons/10000000000+B*epsilons/100000+C
		epsilon=(epsilons/100000)-epsilon_e
		sigma=float('%.2f'%sigma)
		epsilon=float('%.6f'%epsilon)
		list1.append((sigma,epsilon))

	for epsilons in drange(epsilon_e1*10000,epsilon_e2*10000,5):
		sigma=fy
		epsilon=(epsilons/10000)-epsilon_e
		sigma=float('%.2f'%sigma)
		epsilon=float('%.6f'%epsilon)
		list1.append((sigma,epsilon))

	for epsilons in drange(epsilon_e2*1000,epsilon_e3*1000,5):
		sigma=fy*(1+0.6*((epsilons-epsilon_e2*1000)/(epsilon_e3*1000-epsilon_e2*1000)))
		epsilon=(epsilons/1000)-epsilon_e
		sigma=float('%.2f'%sigma)
		epsilon=float('%.6f'%epsilon)
		list1.append((sigma,epsilon))

	for epsilons in drange(epsilon_e3*1000,epsilon_e3*2000,50):
		sigma=1.6*fy
		epsilon=(epsilons/1000)-epsilon_e
		sigma=float('%.2f'%sigma)
		epsilon=float('%.6f'%epsilon)
		list1.append((sigma,epsilon))
	tuple1=tuple(list1)
	#�����ֲĲ���
	steel=myModel.Material(name='Material-steel-tube')
	steel.Density(table=((7.8e-9,),))
	steel.Elastic(table=((206000.0, 0.3),))
	steel.Plastic(table=tuple1)
	
	#������Ե�ֲ�
	fy=fyf
	list1=[]
	tuple1=()
	def drange(start, stop, step):
		r = start 
		while r < (stop-step):
			yield r
			r+= step
	#�ֲĲ��Լ���  ���
	for epsilons in drange(epsilon_e*100000,epsilon_e1*100000,5):
		sigma=-A*epsilons*epsilons/10000000000+B*epsilons/100000+C
		epsilon=(epsilons/100000)-epsilon_e
		sigma=float('%.2f'%sigma)
		epsilon=float('%.6f'%epsilon)
		list1.append((sigma,epsilon))

	for epsilons in drange(epsilon_e1*10000,epsilon_e2*10000,5):
		sigma=fy
		epsilon=(epsilons/10000)-epsilon_e
		sigma=float('%.2f'%sigma)
		epsilon=float('%.6f'%epsilon)
		list1.append((sigma,epsilon))

	for epsilons in drange(epsilon_e2*1000,epsilon_e3*1000,5):
		sigma=fy*(1+0.6*((epsilons-epsilon_e2*1000)/(epsilon_e3*1000-epsilon_e2*1000)))
		epsilon=(epsilons/1000)-epsilon_e
		sigma=float('%.2f'%sigma)
		epsilon=float('%.6f'%epsilon)
		list1.append((sigma,epsilon))

	for epsilons in drange(epsilon_e3*1000,epsilon_e3*2000,50):
		sigma=1.6*fy
		epsilon=(epsilons/1000)-epsilon_e
		sigma=float('%.2f'%sigma)
		epsilon=float('%.6f'%epsilon)
		list1.append((sigma,epsilon))
	tuple1=tuple(list1)
	#�����ֲĲ���
	steel=myModel.Material(name='Material-steel-b_flange')
	steel.Density(table=((7.8e-9,),))
	steel.Elastic(table=((206000.0, 0.3),))
	steel.Plastic(table=tuple1)
	
	#��������ֲ�
	fy=fyw
	list1=[]
	tuple1=()
	def drange(start, stop, step):
		r = start 
		while r < (stop-step):
			yield r
			r+= step
	#�ֲĲ��Լ���  ���
	for epsilons in drange(epsilon_e*100000,epsilon_e1*100000,5):
		sigma=-A*epsilons*epsilons/10000000000+B*epsilons/100000+C
		epsilon=(epsilons/100000)-epsilon_e
		sigma=float('%.2f'%sigma)
		epsilon=float('%.6f'%epsilon)
		list1.append((sigma,epsilon))

	for epsilons in drange(epsilon_e1*10000,epsilon_e2*10000,5):
		sigma=fy
		epsilon=(epsilons/10000)-epsilon_e
		sigma=float('%.2f'%sigma)
		epsilon=float('%.6f'%epsilon)
		list1.append((sigma,epsilon))

	for epsilons in drange(epsilon_e2*1000,epsilon_e3*1000,5):
		sigma=fy*(1+0.6*((epsilons-epsilon_e2*1000)/(epsilon_e3*1000-epsilon_e2*1000)))
		epsilon=(epsilons/1000)-epsilon_e
		sigma=float('%.2f'%sigma)
		epsilon=float('%.6f'%epsilon)
		list1.append((sigma,epsilon))

	for epsilons in drange(epsilon_e3*1000,epsilon_e3*2000,50):
		sigma=1.6*fy
		epsilon=(epsilons/1000)-epsilon_e
		sigma=float('%.2f'%sigma)
		epsilon=float('%.6f'%epsilon)
		list1.append((sigma,epsilon))
	tuple1=tuple(list1)
	#�����ֲĲ���
	steel=myModel.Material(name='Material-steel-b_web')
	steel.Density(table=((7.8e-9,),))
	steel.Elastic(table=((206000.0, 0.3),))
	steel.Plastic(table=tuple1)
	
		
	#���������Լ���  ��ɫ��ʽ
	list2=[]
	tuple2=()
	eta=2   #Բ�ֹܽ���
	sigma0=fc
	epsilon_c=(1300+12.5*fc)*10**(-6)
	epsilon_0=epsilon_c+800*(ksi**0.2)*(10**(-6))
	beta0 = 0.5 * (((2.36 * (10 **(-5))) ** (0.25 + ((ksi - 0.5) ** 7))) * (fc**0.5))
	if beta0 < 0.12:
		beta0 = 0.12
	concretestart=0.3*fc/Ec      #??������ʼ��
	for epsiloncc in drange(concretestart,concretestart+25*0.0002,0.0002):
		x=epsiloncc/epsilon_0
		if x<=1: 
			y=2*x-x**2      
		if x>1:
			y=x/((beta0*((x-1)**eta))+x)
		sigmac=y*sigma0
		epsilonccc=epsiloncc-concretestart
		sigmac=float('%.2f'%sigmac)
		epsilonccc=float('%.6f'%epsilonccc)
		list2.append((sigmac,epsilonccc))
	for epsiloncc in drange(concretestart+25*0.0002,0.1,0.0005):
		x=epsiloncc/epsilon_0
		if x<=1: 
			y=2*x-x**2
		if x>1:
			y=x/((beta0*((x-1)**eta))+x)
		sigmac=y*sigma0
		epsilonccc=epsiloncc-concretestart
		sigmac=float('%.2f'%sigmac)
		epsilonccc=float('%.6f'%epsilonccc)
		list2.append((sigmac,epsilonccc))
	tuple2=tuple(list2)
	#�����ܺͿ���Ӧ���ļ���
	sigmat0 = 0.26*((1.25*fc)**0.666667)
	sigmat0=float('%.3f'%sigmat0)           #ȡС��λ����
	if fcu == 20:
		gfi=0.04
	elif fcu == 40:
		gfi = 0.12
	else:
		gfi=0.004 * fcu - 0.04
	

	#��������������
	concrete=myModel.Material(name='Material-concrete')
	concrete.Density(table=((2.4e-9, ), ))
	concrete.Elastic(table=((EC, 0.2),))
	concrete.ConcreteDamagedPlasticity(table=((30.0, 0.1, 1.16, 0.66667, 1e-05), ))
	concrete.concreteDamagedPlasticity.ConcreteCompressionHardening(table=(tuple2))
	concrete.concreteDamagedPlasticity.ConcreteTensionStiffening(table=((sigmat0, gfi), ), type=GFI)
		
	#�������Ͻ���
	myModel.HomogeneousSolidSection(name='Section-concrete',material='Material-concrete', thickness=None)
	myModel.HomogeneousSolidSection(name='Section-rigid',material='Material-rigid', thickness=None)
	myModel.HomogeneousSolidSection(name='Section-tube',material='Material-steel-tube', thickness=None)
	myModel.HomogeneousSolidSection(name='Section-bolt',material='Material-steel-tube', thickness=None)
	#�Խڵ����ֹܽ�����ǿ��
	#joint_tube_t=((ratio_a+1)**0.5-1)*(diameter/2-thickness)      ������  ��Լ��ЧӦ�й�
	#joint_tube_t=thickness
	myModel.HomogeneousSolidSection(name='Section-joint-tube', material='Material-steel-tube', thickness=None)
	myModel.HomogeneousSolidSection(name='Section-beam-flange', material='Material-steel-b_flange', thickness=None) 
	myModel.HomogeneousSolidSection(name='Section-beam-web', material='Material-steel-b_web', thickness=None)     
	myModel.HomogeneousSolidSection(name='Section-flange', material='Material-steel-tube', thickness=None)	
	
	#���渳��������
	p = myModel.parts['concrete']
	p.SectionAssignment(region=p.sets['concrete'], sectionName='Section-concrete', 
		offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='',thicknessAssignment=FROM_SECTION)
	p = myModel.parts['tube rigid']
	c = p.cells
	cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
	region = regionToolset.Region(cells=cells)
	p.SectionAssignment(region=region, sectionName='Section-rigid', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='',thicknessAssignment=FROM_SECTION)
	
	#���θ������
	p = myModel.parts['beam']
	p.SectionAssignment(region=p.sets['web'], sectionName='Section-beam-web', 
		offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
	p.SectionAssignment(region=p.sets['flange'], sectionName='Section-beam-flange', 
		offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
	
	#�ֹܸ������
	p = myModel.parts['tube']
	p.SectionAssignment(region=p.sets['tube'], sectionName='Section-tube', 
		offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
	#�ڵ㸳�����
	p = myModel.parts['joint']
	#�ڵ�Ļ���   #Section-beam  joint
	p.SectionAssignment(region=p.sets['huanban'], sectionName='Section-beam-flange', 
		offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
	#�ڵ�ĸ���
	p.SectionAssignment(region=p.sets['joint-fuban'], sectionName='Section-beam-web', 
		offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
	#�ڵ�ĸֹܲ���  #Section-tube
	p.SectionAssignment(region=p.sets['joint-tube'], sectionName='Section-joint-tube', 
		offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
	
	#�����������
	p = myModel.parts['flange']
	region = regionToolset.Region(cells=p.cells[0:1])
	p.SectionAssignment(region=region, sectionName='Section-flange', 
		offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
	#��˨�������
	p = myModel.parts['bolt']
	region = regionToolset.Region(cells=p.cells[0:4])
	p.SectionAssignment(region=region, sectionName='Section-bolt', 
		offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
	
	#3 Assemblyģ��
	a = myModel.rootAssembly
	a.DatumCsysByDefault(CARTESIAN)
	p = myModel.parts['beam']
	a.Instance(name='beam-1', part=p, dependent=ON)
	p = myModel.parts['concrete']
	a.Instance(name='concrete-1', part=p, dependent=ON)
	p = myModel.parts['joint']
	a.Instance(name='joint-1', part=p, dependent=ON)
	a = mdb.models['CIJ'].rootAssembly
	a.rotate(instanceList=('joint-1', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, 1.0), angle=90.0)
	p = myModel.parts['tube']
	a.Instance(name='tube-1', part=p, dependent=ON)
	p = myModel.parts['tube rigid']
	a.Instance(name='tube rigid-1', part=p, dependent=ON)
	a.RadialInstancePattern(instanceList=('beam-1', ), point=(0.0, 0.0, 0.0), axis=(0.0, 0.0, 1.0), number=2, totalAngle=360.0)
	a.RadialInstancePattern(instanceList=('tube-1', 'tube rigid-1'), point=(0.0, 0.0, 0.0), axis=(1.0, 0.0, 0.0), number=2, totalAngle=360.0)
	#3.1�����̵�λ��   ע�⵽����ֻ��һ������  ������Ǹ��������Ҫƫ��  ��װ��λ��ʱ��Ҫע�ⷽ��ԭ����ת��
	a = myModel.rootAssembly
	p = myModel.parts['flange']
	a.Instance(name='flange-1', part=p, dependent=ON)
	a.translate(instanceList=('flange-1', ), vector=(0.0, 0.0, b_depth/2))
	a.Instance(name='flange-2', part=p, dependent=ON)
	a.rotate(instanceList=('flange-2', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(1.0, 0.0, 0.0), angle=180.0)
	a.translate(instanceList=('flange-2', ), vector=(0.0, 0.0, -b_depth/2))
	#3.2 ��˨��λ��
	p = myModel.parts['bolt']
	a.Instance(name='bolt-1', part=p, dependent=ON)
	a.translate(instanceList=('bolt-1', ), vector=(0.0, f_Dbolt/2, b_depth/2+flange_t-(flange_t+b_tf)/2))
	a.rotate(instanceList=('bolt-1', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, 1.0), angle=-67.5)
	a.RadialInstancePattern(instanceList=('bolt-1', ), point=(0.0, 0.0, 0.0), axis=(0.0, 0.0, 1.0), number=8, totalAngle=360.0)
	a.Instance(name='bolt-2', part=p, dependent=ON)
	a.rotate(instanceList=('bolt-2', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(1.0, 0.0, 0.0), angle=180)
	a.translate(instanceList=('bolt-2', ), vector=(0.0, f_Dbolt/2, -(b_depth/2+flange_t-(flange_t+b_tf)/2)))
	a.rotate(instanceList=('bolt-2', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, 1.0), angle=-67.5)
	a.RadialInstancePattern(instanceList=('bolt-2', ), point=(0.0, 0.0, 0.0), axis=(0.0, 0.0, 1.0), number=8, totalAngle=360.0)
	#set in assemble
	#a.Surface(side1Faces=a.instances['tube-1-rad-2'].surfaces['tube-inner']+a.instances['joint-1'].surfaces['joint-tube-inner']+a.instances['tube-1'].surfaces['tube-inner'], name='tube-inner')
	s1 = a.instances['joint-1'].faces
	side1Faces1 = s1[9:10]+s1[13:14]+s1[55:56]
	s2 = a.instances['tube-1'].faces
	side1Faces2 = s2[2:3]+s2[4:5]
	s3 = a.instances['tube-1-rad-2'].faces
	side1Faces3 = s3[2:3]+s3[4:5]
	a.Surface(side1Faces=side1Faces1+side1Faces2+side1Faces3, name='tube-inner')
	'''
	#�ױ� X��Y
	name1=list('hole_flange-1')
	name2=list('hole_joint-shang-1')
	name3=list('bolthole-shang-1')
	for i in range(1,9):
		name1[12]=str(i)
		name2[17]=str(i)
		name3[15]=str(i)
		a.Surface(side1Faces=a.instances['flange-1'].surfaces["".join(name1)]+a.instances['joint-1'].surfaces["".join(name2)], name="".join(name3))
	name1=list('hole_flange-1')
	name2=list('hole_joint-xia-1')
	name3=list('bolthole-xia-1')
	for i in range(1,9):
		name1[12]=str(9-i)
		name2[15]=str(i)
		name3[13]=str(i)
		a.Surface(side1Faces=a.instances['flange-1'].surfaces["".join(name1)]+a.instances['joint-1'].surfaces["".join(name2)], name="".join(name3))
	#������ţ�
	'''
	#����ɲ���������?
	a.Surface(side1Faces=a.instances['flange-1'].faces[7:8]+a.instances['joint-1'].faces[47:48], name='bolthole-shang-1')
	a.Surface(side1Faces=a.instances['flange-1'].faces[6:7]+a.instances['joint-1'].faces[54:55], name='bolthole-shang-2')
	a.Surface(side1Faces=a.instances['flange-1'].faces[5:6]+a.instances['joint-1'].faces[53:54], name='bolthole-shang-3')
	a.Surface(side1Faces=a.instances['flange-1'].faces[4:5]+a.instances['joint-1'].faces[52:53], name='bolthole-shang-4')
	a.Surface(side1Faces=a.instances['flange-1'].faces[3:4]+a.instances['joint-1'].faces[51:52], name='bolthole-shang-5')
	a.Surface(side1Faces=a.instances['flange-1'].faces[2:3]+a.instances['joint-1'].faces[50:51], name='bolthole-shang-6')
	a.Surface(side1Faces=a.instances['flange-1'].faces[1:2]+a.instances['joint-1'].faces[49:50], name='bolthole-shang-7')
	a.Surface(side1Faces=a.instances['flange-1'].faces[9:10]+a.instances['joint-1'].faces[48:49], name='bolthole-shang-8')
	
	a.Surface(side1Faces=a.instances['flange-2'].faces[9:10]+a.instances['joint-1'].faces[22:23], name='bolthole-xia-1')
	a.Surface(side1Faces=a.instances['flange-2'].faces[1:2]+a.instances['joint-1'].faces[29:30], name='bolthole-xia-2')
	a.Surface(side1Faces=a.instances['flange-2'].faces[2:3]+a.instances['joint-1'].faces[28:29], name='bolthole-xia-3')
	a.Surface(side1Faces=a.instances['flange-2'].faces[3:4]+a.instances['joint-1'].faces[27:28], name='bolthole-xia-4')
	a.Surface(side1Faces=a.instances['flange-2'].faces[4:5]+a.instances['joint-1'].faces[26:27], name='bolthole-xia-5')
	a.Surface(side1Faces=a.instances['flange-2'].faces[5:6]+a.instances['joint-1'].faces[25:26], name='bolthole-xia-6')
	a.Surface(side1Faces=a.instances['flange-2'].faces[6:7]+a.instances['joint-1'].faces[24:25], name='bolthole-xia-7')
	a.Surface(side1Faces=a.instances['flange-2'].faces[7:8]+a.instances['joint-1'].faces[23:24], name='bolthole-xia-8')

	#4 Step
	myModel.StaticStep(name='S1-Pretension10N', previous='Initial',maxNumInc=500, initialInc=0.01, minInc=1e-09, maxInc=0.1, nlgeom=ON)
	myModel.StaticStep(name='S2-Pretension15kN', previous='S1-Pretension10N',timePeriod=1, maxNumInc=500, initialInc=0.01, minInc=1e-09, maxInc=0.1, nlgeom=ON)
	myModel.StaticStep(name='S3-FixBoltLength', previous='S2-Pretension15kN',timePeriod=1, maxNumInc=500, initialInc=0.01, minInc=1e-09, maxInc=0.1, nlgeom=ON)
	myModel.StaticStep(name='axial load', previous='S3-FixBoltLength',timePeriod=1, maxNumInc=500, initialInc=0.01, minInc=1e-09, maxInc=0.1, nlgeom=ON)
	myModel.StaticStep(name='cyclic load', previous='axial load',timePeriod=1, maxNumInc=2000, initialInc=0.00001, minInc=1e-09, maxInc=0.05, nlgeom=ON)   #nlgeom���η�����
	#4'���̱����ͳ���������  ��Ĭ�ϵ���

	#5 interaction
	#5.1 create interaction properties
	myModel.ContactProperty('concrete-tube')
	myModel.interactionProperties['concrete-tube'].NormalBehavior(pressureOverclosure=HARD, allowSeparation=ON,constraintEnforcementMethod=DEFAULT)
	myModel.interactionProperties['concrete-tube'].TangentialBehavior(
		formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF,
		pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, table=((0.25, ), ), 
		shearStressLimit=None, maximumElasticSlip=FRACTION,fraction=0.005, elasticSlipStiffness=None)
	myModel.ContactProperty('flange')
	myModel.interactionProperties['flange'].TangentialBehavior(
		formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
		pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, table=((0.15, ), ), 
		shearStressLimit=None, maximumElasticSlip=FRACTION, fraction=0.005, elasticSlipStiffness=None)
	myModel.interactionProperties['flange'].NormalBehavior(pressureOverclosure=HARD, allowSeparation=ON, constraintEnforcementMethod=DEFAULT)

#5.2 concrete-tube
	myModel.SurfaceToSurfaceContactStd(name='concrete-tube', createStepName='Initial', 
		master=a.surfaces['tube-inner'],
		slave=a.instances['concrete-1'].surfaces['surface-all'], 
		sliding=FINITE, thickness=OFF, interactionProperty='concrete-tube', adjustMethod=OVERCLOSED, initialClearance=OMIT, datumAxis=None, clearanceRegion=None, tied=OFF)

#5.3 �ֹ�����ذ�
	myModel.Tie(name='tube-rigid-1', 
		master=a.instances['tube rigid-1'].surfaces['bottom'], 
		slave=a.instances['tube-1'].surfaces['tube-rigid'], 
		positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=OFF)
	myModel.Tie(name='tube-rigid-2', 
		master=a.instances['tube rigid-1-rad-2'].surfaces['bottom'], 
		slave=a.instances['tube-1-rad-2'].surfaces['tube-rigid'], 
		positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=OFF)
#���ذ�ͻ�����
	myModel.Tie(name='rigid-concrete-1', 
		master=a.instances['tube rigid-1'].surfaces['bottom'], 
		slave=a.instances['concrete-1'].surfaces['top'],  
		positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=OFF)
	myModel.Tie(name='rigid-concrete-2', 
		master=a.instances['tube rigid-1-rad-2'].surfaces['bottom'], 
		slave=a.instances['concrete-1'].surfaces['bottom'],  
		positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=OFF)
 
#5.4�ڵ� ��
	myModel.Tie(name='joint-beam+y', 
		master=a.instances['beam-1'].surfaces['beam-inner'], 
		slave=a.instances['joint-1'].surfaces['joint I y+'], 
		positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=OFF)
	myModel.Tie(name='joint-beam-y', 
		master=a.instances['beam-1-rad-2'].surfaces['beam-inner'],  
		slave=a.instances['joint-1'].surfaces['joint I y-'], 
		positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=OFF)
	
#5.5flange-flange
	myModel.SurfaceToSurfaceContactStd(name='f-f-1', 
		createStepName='Initial', 
		master=a.instances['flange-1'].surfaces['f-f'],  
		slave=a.instances['joint-1'].surfaces['huanban-uu'],  
		sliding=FINITE, thickness=ON, interactionProperty='flange', adjustMethod=NONE, initialClearance=OMIT, datumAxis=None, clearanceRegion=None)
	myModel.SurfaceToSurfaceContactStd(name='f-f-2', 
		createStepName='Initial', 
		master=a.instances['flange-2'].surfaces['f-f'],  
		slave=a.instances['joint-1'].surfaces['huanban-dd'],  
		sliding=FINITE, thickness=ON, interactionProperty='flange', adjustMethod=NONE, initialClearance=OMIT, datumAxis=None, clearanceRegion=None)
#5.6 bolt
		#bolt-b_flange
		#bolt-hole
		#bolt-joint_flange
	#bolt-flange-shang
	myModel.SurfaceToSurfaceContactStd(name='bolt-flange-shang-1', 
		createStepName='Initial', 
		master=a.instances['flange-1'].surfaces['flange-Zouter'], 
		slave=a.instances['bolt-1'].surfaces['bolt-b_flange'],  
		sliding=FINITE, thickness=ON, interactionProperty='flange', adjustMethod=NONE, initialClearance=OMIT, datumAxis=None, clearanceRegion=None)
   	
	name1=list('bolt-flange-shang-1')
	name2=list('bolt-1-rad-2')
	for i in range(2,9):
		name1[18]=str(i)
		name2[11]=str(i)
		myModel.SurfaceToSurfaceContactStd(name="".join(name1), 
			createStepName='Initial', 
			master=a.instances['flange-1'].surfaces['flange-Zouter'], 
			slave=a.instances["".join(name2)].surfaces['bolt-b_flange'],  
			sliding=FINITE, thickness=ON, interactionProperty='flange', adjustMethod=NONE, initialClearance=OMIT, datumAxis=None, clearanceRegion=None)

#bolt-flange-xia
	myModel.SurfaceToSurfaceContactStd(name='bolt-flange-xia-1', 
		createStepName='Initial', 
		master=a.instances['flange-2'].surfaces['flange-Zouter'], 
		slave=a.instances['bolt-2'].surfaces['bolt-b_flange'],  
		sliding=FINITE, thickness=ON, interactionProperty='flange', adjustMethod=NONE, initialClearance=OMIT, datumAxis=None, clearanceRegion=None)
   	
	name1=list('bolt-flange-xia-1')
	name2=list('bolt-2-rad-2')
	for i in range(2,9):
		name1[16]=str(i)
		name2[11]=str(i)
		myModel.SurfaceToSurfaceContactStd(name="".join(name1), 
			createStepName='Initial', 
			master=a.instances['flange-2'].surfaces['flange-Zouter'], 
			slave=a.instances["".join(name2)].surfaces['bolt-b_flange'],  
			sliding=FINITE, thickness=ON, interactionProperty='flange', adjustMethod=NONE, initialClearance=OMIT, datumAxis=None, clearanceRegion=None)				

#bolt-joint-shang
	myModel.SurfaceToSurfaceContactStd(name='bolt-joint-shang-1', 
		createStepName='Initial', 
		master=a.instances['joint-1'].surfaces['huanban-ud'], 
		slave=a.instances['bolt-1'].surfaces['bolt-joint_flange'],  
		sliding=FINITE, thickness=ON, interactionProperty='flange', adjustMethod=NONE, initialClearance=OMIT, datumAxis=None, clearanceRegion=None)
   	
	name1=list('bolt-joint-shang-1')
	name2=list('bolt-1-rad-2')
	for i in range(2,9):
		name1[17]=str(i)
		name2[11]=str(i)
		myModel.SurfaceToSurfaceContactStd(name="".join(name1), 
			createStepName='Initial', 
			master=a.instances['joint-1'].surfaces['huanban-ud'],
			slave=a.instances["".join(name2)].surfaces['bolt-joint_flange'],  
			sliding=FINITE, thickness=ON, interactionProperty='flange', adjustMethod=NONE, initialClearance=OMIT, datumAxis=None, clearanceRegion=None)	

#bolt-joint-xia
	myModel.SurfaceToSurfaceContactStd(name='bolt-joint-xia-1', 
		createStepName='Initial', 
		master=a.instances['joint-1'].surfaces['huanban-du'], 
		slave=a.instances['bolt-2'].surfaces['bolt-joint_flange'],  
		sliding=FINITE, thickness=ON, interactionProperty='flange', adjustMethod=NONE, initialClearance=OMIT, datumAxis=None, clearanceRegion=None)
   	
	name1=list('bolt-joint-xia-1')
	name2=list('bolt-2-rad-2')
	for i in range(2,9):
		name1[15]=str(i)
		name2[11]=str(i)
		myModel.SurfaceToSurfaceContactStd(name="".join(name1), 
			createStepName='Initial', 
			master=a.instances['joint-1'].surfaces['huanban-du'],
			slave=a.instances["".join(name2)].surfaces['bolt-joint_flange'],  
			sliding=FINITE, thickness=ON, interactionProperty='flange', adjustMethod=NONE, initialClearance=OMIT, datumAxis=None, clearanceRegion=None)	

#5.7 bolt hole
	myModel.SurfaceToSurfaceContactStd(name='bolthole-shang-1', 
		createStepName='Initial', 
		master=a.surfaces['bolthole-shang-1'], 
		slave=a.instances['bolt-1'].surfaces['bolt-hole'],  
		sliding=FINITE, thickness=ON, interactionProperty='flange', adjustMethod=NONE, initialClearance=OMIT, datumAxis=None, clearanceRegion=None)
   	
	name1=list('bolthole-shang-1')
	name2=list('bolt-1-rad-1')
	for i in range(2,9):
		name1[15]=str(i)
		name2[11]=str(i)
		myModel.SurfaceToSurfaceContactStd(name="".join(name1), 
			createStepName='Initial', 
			master=a.surfaces["".join(name1)], 
			slave=a.instances["".join(name2)].surfaces['bolt-hole'],  
			sliding=FINITE, thickness=ON, interactionProperty='flange', adjustMethod=NONE, initialClearance=OMIT, datumAxis=None, clearanceRegion=None)	
	
	myModel.SurfaceToSurfaceContactStd(name='bolthole-xia-1', 
		createStepName='Initial', 
		master=a.surfaces['bolthole-xia-1'], 
		slave=a.instances['bolt-2'].surfaces['bolt-hole'],  
		sliding=FINITE, thickness=ON, interactionProperty='flange', adjustMethod=NONE, initialClearance=OMIT, datumAxis=None, clearanceRegion=None)	
	name1=list('bolthole-xia-1')
	name2=list('bolt-2-rad-1')
	for i in range(2,9):
		name1[13]=str(i)
		name2[11]=str(i)
		myModel.SurfaceToSurfaceContactStd(name="".join(name1), 
			createStepName='Initial', 
			master=a.surfaces["".join(name1)], 
			slave=a.instances["".join(name2)].surfaces['bolt-hole'],  
			sliding=FINITE, thickness=ON, interactionProperty='flange', adjustMethod=NONE, initialClearance=OMIT, datumAxis=None, clearanceRegion=None)	

#5.8flange-tube
	myModel.Tie(name='tube-flange-shang', 
		master=a.instances['flange-1'].surfaces['flange-inner'], 
		slave=a.instances['tube-1'].surfaces['tube-flange'], 
		positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=OFF)
	myModel.Tie(name='tube-flange-xia', 
		master=a.instances['flange-2'].surfaces['flange-inner'], 
		slave=a.instances['tube-1-rad-2'].surfaces['tube-flange'], 
		positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=OFF)
	
	#5.5 ������ϵ�  �����ȡ����             ��ϵ��λ����Ҫ�úÿ���
	RPzuo=a.ReferencePoint(point=(0, -0.54*b_span, -0.6*b_depth))
	RPyou=a.ReferencePoint(point=(0, 0.54*b_span, 0.6*b_depth))
	r = a.referencePoints
	a.Set(referencePoints=(r[RPzuo.id], ), name='RPzuo')     #�����ʽ���о�һ��
	a.Set(referencePoints=(r[RPyou.id], ), name='RPyou')
	#���          ��ȫ��������
	region1=a.sets['RPzuo']
	region2=a.instances['beam-1-rad-2'].surfaces['beam-outer']
	myModel.Coupling(name='Coupling-zuo', 
		controlPoint=region1, surface=region2, influenceRadius=WHOLE_SURFACE, 
		couplingType=KINEMATIC, localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)
	region1=a.sets['RPyou']
	region2=a.instances['beam-1'].surfaces['beam-outer']
	myModel.Coupling(name='Coupling-you', 
		controlPoint=region1, surface=region2, influenceRadius=WHOLE_SURFACE, 
		couplingType=KINEMATIC, localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)
	
	#6load
	#6.1���¶˰�  initial λ��Լ��         �߽�����Ū����һ��  ����YZƽ��ת��
	f = a.instances['tube rigid-1-rad-2'].faces
	faces = f.getSequenceFromMask(mask=('[#2 ]', ), )
	region = regionToolset.Region(faces=faces)
	myModel.DisplacementBC(name='bottom', createStepName='Initial', region=region, 
	u1=SET, u2=SET, u3=SET, ur1=UNSET, ur2=SET, ur3=SET, 
	amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
	f = a.instances['tube rigid-1'].faces
	faces = f.getSequenceFromMask(mask=('[#2 ]', ), )
	region = regionToolset.Region(faces=faces)
	myModel.DisplacementBC(name='top', createStepName='Initial', region=region, 
	u1=SET, u2=SET, u3=UNSET, ur1=UNSET, ur2=SET, ur3=SET, 
	amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
	
	#6.2 axial load
	s1 = a.instances['tube rigid-1'].faces
	side1Faces1 = s1.getSequenceFromMask(mask=('[#2 ]', ), )
	region = regionToolset.Region(side1Faces=side1Faces1)
	myModel.Pressure(name='No', createStepName='axial load', region=region, distributionType=TOTAL_FORCE, field='', magnitude=load, amplitude=UNSET)
	
	#6.3 cyclic displacement   ��Ҫȥ����ϼ���ֱ�Ӹ����������   ��ϵ����ܹ�����ƽ����ת���Ľ�  ���ﻹ��Ҫ����һ��
	#�������ط�ֵ����   ÿ�ַ�ֵ�ظ�����
	myModel.EquallySpacedAmplitude(name='cyclic', timeSpan=STEP, smooth=SOLVER_DEFAULT, fixedInterval=0.25, begin=0.0, 
		data=(0.0, 1.0, 0.0, -1.0, 0.0, 1.0, 0.0, -1.0, 0.0, 1.0, 0.0, -1.0,
			  0.0, 2.0, 0.0, -2.0, 0.0, 2.0, 0.0, -2.0, 0.0, 2.0, 0.0, -2.0,
			  0.0, 3.0, 0.0, -3.0, 0.0, 3.0, 0.0, -3.0, 0.0, 3.0, 0.0, -3.0, 
			  0.0))   #3x3
	#����λ�Ƽ��صľֲ�����ϵ   ��ȫ������ϵ���ز��ԣ�λ�����������ġ�������һ���취���������ģ�͵����ĵ㣬�����һ����̬�ĵ���ܻ���ִ���������̫��
	#r = a.referencePoints
	#DCleft=a.DatumCsysByThreePoints(origin=r[RPzuo.id], name='DCleft', coordSysType=CARTESIAN, line1=(1.0, 0.0, 0.0), line2=(0.0, 1.0, 0.0))
	#datum = myModel.rootAssembly.datums[DCleft.id]
	#����λ�ƺ���    localCsys=Noneָ����Ĭ��ȫ������ϵ
	#amplitude='cyclic' UNSET
	myModel.DisplacementBC(name='cyc-y+z',createStepName='cyclic load', region=a.sets['RPzuo'], 
						   u1=0.0, u2=UNSET, u3=displacement, 
	                       ur1=UNSET, ur2=0, ur3=0, amplitude=UNSET, fixed=OFF,
	                       distributionType=UNIFORM, fieldName='', localCsys=None)
	myModel.DisplacementBC(name='cyc+y-z',createStepName='cyclic load', region=a.sets['RPyou'], 
						   u1=0.0, u2=UNSET, u3=-displacement, 
	                       ur1=UNSET, ur2=0, ur3=0, amplitude=UNSET, fixed=OFF,
	                       distributionType=UNIFORM, fieldName='', localCsys=None)
#6.3��˨����
	region = regionToolset.Region(side1Faces=a.instances['bolt-1'].faces[0:1])
	datumAxis = myModel.rootAssembly.datums[1].axis3
	myModel.BoltLoad(name='Load Pretension-1', createStepName='S1-Pretension10N', region=region, magnitude=10.0, boltMethod=APPLY_FORCE, datumAxis=datumAxis)
	myModel.loads['Load Pretension-1'].setValuesInStep(stepName='S2-Pretension15kN', magnitude=7500.0, boltMethod=APPLY_FORCE)
	myModel.loads['Load Pretension-1'].setValuesInStep(stepName='S3-FixBoltLength', boltMethod=FIX_LENGTH)
	name1=list('bolt-1-rad-2')
	name2=list('Load Pretension-2')
	for i in range(2,9):
		name1[11]=str(i)
		name2[16]=str(i)
		region = regionToolset.Region(side1Faces=a.instances["".join(name1)].faces[0:1])
		datumAxis = myModel.rootAssembly.datums[1].axis3
		myModel.BoltLoad(name="".join(name2), createStepName='S1-Pretension10N', region=region, magnitude=10.0, boltMethod=APPLY_FORCE, datumAxis=datumAxis)
		myModel.loads["".join(name2)].setValuesInStep(stepName='S2-Pretension15kN', magnitude=7500.0, boltMethod=APPLY_FORCE)
		myModel.loads["".join(name2)].setValuesInStep(stepName='S3-FixBoltLength', boltMethod=FIX_LENGTH)
	
	region = regionToolset.Region(side1Faces=a.instances['bolt-2'].faces[0:1])
	datumAxis = myModel.rootAssembly.datums[1].axis3
	myModel.BoltLoad(name='Load Pretension-xia-1', createStepName='S1-Pretension10N', region=region, magnitude=10.0, boltMethod=APPLY_FORCE, datumAxis=datumAxis)
	myModel.loads['Load Pretension-xia-1'].setValuesInStep(stepName='S2-Pretension15kN', magnitude=7500.0, boltMethod=APPLY_FORCE)
	myModel.loads['Load Pretension-xia-1'].setValuesInStep(stepName='S3-FixBoltLength', boltMethod=FIX_LENGTH)
	name1=list('bolt-2-rad-2')
	name2=list('Load Pretension-xia-2')
	for i in range(2,9):
		name1[11]=str(i)
		name2[20]=str(i)
		region = regionToolset.Region(side1Faces=a.instances["".join(name1)].faces[0:1])
		datumAxis = myModel.rootAssembly.datums[1].axis3
		myModel.BoltLoad(name="".join(name2), createStepName='S1-Pretension10N', region=region, magnitude=10.0, boltMethod=APPLY_FORCE, datumAxis=datumAxis)
		myModel.loads["".join(name2)].setValuesInStep(stepName='S2-Pretension15kN', magnitude=7500.0, boltMethod=APPLY_FORCE)
		myModel.loads["".join(name2)].setValuesInStep(stepName='S3-FixBoltLength', boltMethod=FIX_LENGTH)	
		

#7 mesh-���񻮷�                      aΪ#Assemblyģ��a = myModel.rootAssembly  a��p  ȫ����ֲ�
	meshsize=30
#7.1 beam-�������񻮷�
	p = myModel.parts['beam']
	p.seedPart(size=meshsize, deviationFactor=0.1, minSizeFactor=0.1)
	e = p.edges
	p.seedEdgeByNumber(edges=e[33:34]+e[41:42]+e[53:54]+e[61:62], number=6, constraint=FINER)
	p.seedEdgeByNumber(edges=e[49:50], number=10, constraint=FINER)
	p.seedEdgeByNumber(edges=e[19:20], number=30, constraint=FINER)
	p.setMeshControls(regions=p.cells[0:6], technique=SWEEP, algorithm=ADVANCING_FRONT)
	p.generateMesh()
#7.2 bolt mesh
	p = myModel.parts['bolt']
	p.seedPart(size=5, deviationFactor=0.1, minSizeFactor=0.1)
	p.seedEdgeByNumber(edges=p.edges[0:1], number=12, constraint=FINER)	
	p.generateMesh()
#7.3 concrete���������񻮷�
	p = myModel.parts['concrete']
	p.seedPart(size=30, deviationFactor=0.1, minSizeFactor=0.1)
	p.seedEdgeByNumber(edges=p.edges[0:2], number=30, constraint=FINER)
	p.setMeshControls(regions=p.cells[0:1], algorithm=ADVANCING_FRONT)
	p.generateMesh()
#7.4flange
	p = myModel.parts['flange']
	c = p.cells
	p.setMeshControls(regions=c[0:1], algorithm=ADVANCING_FRONT)
	p.seedPart(size=0.5*meshsize, deviationFactor=0.1, minSizeFactor=0.1) 
	e = p.edges
	p.seedEdgeByNumber(edges=e[16:18], number=50, constraint=FINER)
	p.seedEdgeByNumber(edges=e[2:16]+e[18:20], number=12, constraint=FINER)
	#e[2:3]+e[4:5]+e[6:7]+e[8:9]+e[10:11]+e[12:13]+e[14:15]+e[16:17]
	p.generateMesh()
#7.5joint  
	p = myModel.parts['joint']
	p.seedPart(size=0.5*meshsize, deviationFactor=0.1, minSizeFactor=0.1)
	p.setMeshControls(regions=p.cells[0:5], algorithm=ADVANCING_FRONT)
	e = p.edges
	p.seedEdgeByNumber(edges=e[90:94]+e[98:102]+e[115:123], number=12, constraint=FINER)
	p.seedEdgeByNumber(edges=e[53:57]+e[60:64]+e[74:82], number=12, constraint=FINER)
	p.seedEdgeByNumber(edges=e[26:27]+e[36:37]+e[39:40]+e[123:124], number=50, constraint=FINER)
	p.seedEdgeByNumber(edges=e[37:39], number=25, constraint=FINER) 
	p.seedEdgeByNumber(edges=e[27:28]+e[31:32]+e[40:41]+e[44:46]+e[49:50]+e[89:90]+e[94:95], number=6, constraint=FINER)
	p.generateMesh()
#7.6 tube
	p = myModel.parts['tube']
	p.seedPart(size=40, deviationFactor=0.1, minSizeFactor=0.1)
	p.seedEdgeByNumber(edges=p.edges[0:4], number=30, constraint=FINER)
	p.setMeshControls(regions=p.cells[0:2], algorithm=ADVANCING_FRONT)
	p.generateMesh()
#7.7 tube rigid-���˰����񻮷�    #Ӧ�øĸ����� column
	p = myModel.parts['tube rigid']
	p.seedPart(size=40, deviationFactor=0.1, minSizeFactor=0.1)
	p.seedEdgeByNumber(edges=p.edges[0:2], number=30, constraint=FINER)
	p.setMeshControls(regions=p.cells[0:1], algorithm=ADVANCING_FRONT)
	p.generateMesh()
	#�ύjob               #�ڲ�ͬ�ĵ����ϼǵð��̸߳�һ��
	mdb.Job(name=jobname, model=Modelname, description='', type=ANALYSIS, 
		atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=85, 
		memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
		explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
		modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
		scratch='', multiprocessingMode=THREADS, numCpus=8, numDomains=8)
#��ͼ������Ļ
