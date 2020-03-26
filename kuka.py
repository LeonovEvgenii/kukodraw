# import matplotlib.pyplot as plt

_dat = ''
_src = ''

# _plot_x_lin = []
# _plot_y_lin = []

# _plot_xs = []
# _plot_ys = []


n_point = 1

z = 0

def draw(x1,y1,x2,y2):
    
    global _dat
    global _src
    global n_point
    global z
   

    _dat += 'DECL E6POS XP%s={X %s,Y %s,Z %s,A -180,B 0,C 180,S 2,T 10,E1 0.0,E2 0.0,E3 0.0,E4 0.0,E5 0.0,E6 0.0}\n' % (n_point, x1, y1, z)
    _dat += 'DECL FDAT FP%s={TOOL_NO 1,BASE_NO 0,IPO_FRAME #BASE,POINT2[] " "}\n' % n_point
    _dat += 'DECL LDAT LCPDAT%s={VEL 2.00000,ACC 100.000,APO_DIST 500.000,APO_FAC 50.0000,AXIS_VEL 100.000,AXIS_ACC 100.000,ORI_TYP #VAR,CIRC_TYP #BASE,JERK_FAC 50.0000,GEAR_JERK 100.000,EXAX_IGN 0}\n' % n_point

    _src += '''
;FOLD LIN P%s Vel=2 m/s CPDAT%s Tool[1]:marker Base[0] ;%%{PE}
;FOLD Parameters ;%%{h}
;Params IlfProvider=kukaroboter.basistech.inlineforms.movement.old; Kuka.IsGlobalPoint=False; Kuka.PointName=P%s; Kuka.BlendingEnabled=False; Kuka.MoveDataName=CPDAT1; Kuka.VelocityPath=2; Kuka.CurrentCDSetIndex=0; Kuka.MovementParameterFieldEnabled=True; IlfCommand=LIN
;ENDFOLD
$BWDSTART = FALSE
LDAT_ACT = LCPDAT%s
FDAT_ACT = FP%s
BAS(#CP_PARAMS, 2.0)
SET_CD_PARAMS (0)
LIN XP%s
;ENDFOLD
''' % ((n_point, ) * 6)

    n_point += 1

    _dat += 'DECL E6POS XP%s={X %s,Y %s,Z %s,A -180,B 0,C 180,S 2,T 10,E1 0.0,E2 0.0,E3 0.0,E4 0.0,E5 0.0,E6 0.0}\n' % (n_point, x2, y2, z)
    _dat += 'DECL FDAT FP%s={TOOL_NO 1,BASE_NO 0,IPO_FRAME #BASE,POINT2[] " "}\n' % n_point
    _dat += 'DECL LDAT LCPDAT%s={VEL 2.00000,ACC 100.000,APO_DIST 500.000,APO_FAC 50.0000,AXIS_VEL 100.000,AXIS_ACC 100.000,ORI_TYP #VAR,CIRC_TYP #BASE,JERK_FAC 50.0000,GEAR_JERK 100.000,EXAX_IGN 0}\n' % n_point

    _src += '''
;FOLD LIN P%s Vel=2 m/s CPDAT%s Tool[1]:marker Base[0] ;%%{PE}
;FOLD Parameters ;%%{h}
;Params IlfProvider=kukaroboter.basistech.inlineforms.movement.old; Kuka.IsGlobalPoint=False; Kuka.PointName=P%s; Kuka.BlendingEnabled=False; Kuka.MoveDataName=CPDAT1; Kuka.VelocityPath=2; Kuka.CurrentCDSetIndex=0; Kuka.MovementParameterFieldEnabled=True; IlfCommand=LIN
;ENDFOLD
$BWDSTART = FALSE
LDAT_ACT = LCPDAT%s
FDAT_ACT = FP%s
BAS(#CP_PARAMS, 2.0)
SET_CD_PARAMS (0)
LIN XP%s
;ENDFOLD
''' % ((n_point, ) * 6)

    n_point += 1

    
def down():
    global z
    z = -17.64


def up():
    global z
    # global _plot_x_lin
    # global _plot_y_lin
    # global _plot_xs
    # global _plot_ys

    # _plot_xs.append(_plot_x_lin)
    # _plot_ys.append(_plot_y_lin)

    # _plot_x_lin = []
    # _plot_y_lin = []    

    z = -15


def begin(x, y, total_xp):
    
    global _dat
    global _src
    global n_point
    global z

    _dat = '''&ACCESS RVP
&REL 5
&PARAM EDITMASK = *)
&PARAM TEMPLATE = C:\KRC\Roboter\Template\\vorgabe
&PARAM DISKPATH = KRC:\R1\\user programm\demonstration
DEFDAT  test_face
;FOLD EXTERNAL DECLARATIONS;%{PE}%MKUKATPBASIS,%CEXT,%VCOMMON,%P
;FOLD BASISTECH EXT;%{PE}%MKUKATPBASIS,%CEXT,%VEXT,%P
EXT  BAS (BAS_COMMAND  :IN,REAL  :IN )
DECL INT SUCCESS
;ENDFOLD (BASISTECH EXT)
;FOLD USER EXT;%{E}%MKUKATPUSER,%CEXT,%VEXT,%P
;Make your modifications here
;ENDFOLD (USER EXT)
;ENDFOLD (EXTERNAL DECLARATIONS)
 '''

    _dat += '''
    
DECL E6POS XP%s={X %s,Y %s,Z %s,A -180,B 0,C 180,S 2,T 35,E1 0.0,E2 0.0,E3 0.0,E4 0.0,E5 0.0,E6 0.0}
DECL FDAT FP%s={TOOL_NO 1,BASE_NO 0,IPO_FRAME #BASE,POINT2[] " "}
DECL LDAT LCPDAT1={VEL 2.00000,ACC 100.000,APO_DIST 500.000,APO_FAC 50.0000,AXIS_VEL 100.000,AXIS_ACC 100.000,ORI_TYP #VAR,CIRC_TYP #BASE,JERK_FAC 50.0000,GEAR_JERK 100.000,EXAX_IGN 0}
DECL MODULEPARAM_T LAST_TP_PARAMS={PARAMS[] "Kuka.PointName=P%s; Kuka.FrameData.base_no=0; Kuka.FrameData.tool_no=1; Kuka.FrameData.ipo_frame=#BASE; Kuka.isglobalpoint=False; Kuka.MoveDataName=CPDAT4; Kuka.MovementData.apo_fac=50; Kuka.MovementData.apo_dist=500; Kuka.MovementData.axis_acc=100; Kuka.MovementData.axis_vel=100; Kuka.MovementData.circ_typ=#BASE; Kuka.MovementData.jerk_fac=50; Kuka.MovementData.ori_typ=#VAR; Kuka.MovementData.vel=2; Kuka.MovementData.acc=100; Kuka.MovementData.exax_ign=0; Kuka.VelocityPath=2; Kuka.BlendingEnabled=False; Kuka.CurrentCDSetIndex=0      "}
''' % (n_point, x, y, z, n_point, n_point)

    _src = '''&ACCESS RVP
&REL 5
&PARAM EDITMASK = *
&PARAM TEMPLATE = C:\KRC\Roboter\Template\\vorgabe
&PARAM DISKPATH = KRC:\R1\\user programm\demonstration
DEF test_face( )
;FOLD INI;%{PE}
  ;FOLD BASISTECH INI
    GLOBAL INTERRUPT DECL 3 WHEN $STOPMESS==TRUE DO IR_STOPM ( )
    INTERRUPT ON 3 
    BAS (#INITMOV,0 )
  ;ENDFOLD (BASISTECH INI)
  ;FOLD USER INI
    ;Make your modifications here

  ;ENDFOLD (USER INI)
;ENDFOLD (INI)
'''

    _src += '''
;FOLD SPTP HOME Vel=30 % DEFAULT ;%{PE}
;FOLD Parameters ;%{h}
;Params IlfProvider=kukaroboter.basistech.inlineforms.movement.spline; Kuka.IsGlobalPoint=False; Kuka.PointName=HOME; Kuka.BlendingEnabled=False; Kuka.MoveDataPtpName=DEFAULT; Kuka.VelocityPtp=100; Kuka.VelocityFieldEnabled=True; Kuka.CurrentCDSetIndex=0; Kuka.MovementParameterFieldEnabled=True; IlfCommand=SPTP
;ENDFOLD
SPTP XHOME WITH $VEL_AXIS[1] = SVEL_JOINT(100.0), $TOOL = STOOL2(FHOME), $BASE = SBASE(FHOME.BASE_NO), $IPO_MODE = SIPO_MODE(FHOME.IPO_FRAME), $LOAD = SLOAD(FHOME.TOOL_NO), $ACC_AXIS[1] = SACC_JOINT(PDEFAULT), $APO = SAPO_PTP(PDEFAULT), $GEAR_JERK[1] = SGEAR_JERK(PDEFAULT), $COLLMON_TOL_PRO[1] = USE_CM_PRO_VALUES(0)
;ENDFOLD
'''

    _src += '''
;FOLD LIN P%s Vel=2 m/s CPDAT%s Tool[1]:marker Base[0] ;%%{PE}
;FOLD Parameters ;%%{h}
;Params IlfProvider=kukaroboter.basistech.inlineforms.movement.old; Kuka.IsGlobalPoint=False; Kuka.PointName=P%s; Kuka.BlendingEnabled=False; Kuka.MoveDataName=CPDAT1; Kuka.VelocityPath=2; Kuka.CurrentCDSetIndex=0; Kuka.MovementParameterFieldEnabled=True; IlfCommand=LIN
;ENDFOLD
$BWDSTART = FALSE
LDAT_ACT = LCPDAT%s
FDAT_ACT = FP%s
BAS(#CP_PARAMS, 2.0)
SET_CD_PARAMS (0)
LIN XP%s
;ENDFOLD
''' % ((n_point, ) * 6)

    n_point += 1

def end():

    global _src
    global _dat

    _src +='''

;FOLD SPTP HOME Vel=30 % DEFAULT ;%{PE}
;FOLD Parameters ;%{h}
;Params IlfProvider=kukaroboter.basistech.inlineforms.movement.spline; Kuka.IsGlobalPoint=False; Kuka.PointName=HOME; Kuka.BlendingEnabled=False; Kuka.MoveDataPtpName=DEFAULT; Kuka.VelocityPtp=100; Kuka.VelocityFieldEnabled=True; Kuka.CurrentCDSetIndex=0; Kuka.MovementParameterFieldEnabled=True; IlfCommand=SPTP
;ENDFOLD
SPTP XHOME WITH $VEL_AXIS[1] = SVEL_JOINT(100.0), $TOOL = STOOL2(FHOME), $BASE = SBASE(FHOME.BASE_NO), $IPO_MODE = SIPO_MODE(FHOME.IPO_FRAME), $LOAD = SLOAD(FHOME.TOOL_NO), $ACC_AXIS[1] = SACC_JOINT(PDEFAULT), $APO = SAPO_PTP(PDEFAULT), $GEAR_JERK[1] = SGEAR_JERK(PDEFAULT), $COLLMON_TOL_PRO[1] = USE_CM_PRO_VALUES(0)
;ENDFOLD

END
'''

    _dat += 'ENDDAT'


def geometric_transformation(in_list):

    in_list_without_pass = [ _ for _ in in_list if _ ]

    in_list_reverce = []
    for pline in in_list_without_pass:
        pline_temp = []
        for line in pline:
            line_temp = []
            for point in line:
                line_temp.append([point[1], point[0]])
            pline_temp.append(line_temp)
        in_list_reverce.append(pline_temp)

    min_x, min_y, max_x, max_y = 100000,100000,0,0
    for pline in in_list_reverce:
        for line in pline:
            for point in line:
                if min_x > point[0]:    
                    min_x = point[0]
                if min_y > point[1]:    
                    min_y = point[1]
                if max_x < point[0]:    
                    max_x = point[0]
                if max_y < point[1]:    
                    max_y = point[1]
    
    in_list_shift = []
    for pline in in_list_reverce:
        pline_temp = []
        for line in pline:
            line_temp = []
            for point in line:
                # line_temp.append([point[0] * s + dx, point[1] * s + dy])
                line_temp.append([point[0] - min_x, point[1] - min_y])
            pline_temp.append(line_temp)
        in_list_shift.append(pline_temp)


    real_min_x =  280
    real_min_y = -155
    real_max_x =  480
    real_max_y =  155

    # 480 - 280 = 200
    # 155 - (-155) = 300

    dx = max_x - min_x
    dy = max_y - min_y

    sx = 200 / dx
    sy = 300 / dy

    scale = min(sx, sy)

    # dx = real_min_x - min_x
    # dy = real_min_y - min_y

    # sx = (real_max_x - real_min_x)/(max_x - min_x)
    # sy = (real_max_y - real_min_y)/(max_y - min_y)

    # s = sx if sx < sy else sy

    in_list_temp = []
    for pline in in_list_shift:
        pline_temp = []
        for line in pline:
            line_temp = []
            for point in line:
                # line_temp.append([point[0] * s + dx, point[1] * s + dy])
                line_temp.append([point[0] * scale + 280, point[1] * scale  - 155])
            pline_temp.append(line_temp)
        in_list_temp.append(pline_temp)

    return in_list_temp


def gen_kuka_code(raw_list):
    
    global n_point
    global _plot_xs
    global _plot_ys

    global _plot_x_lin
    global _plot_y_lin


    in_list = geometric_transformation(raw_list)

    down()

    total_xp = 0;
    for pline in in_list:
        total_xp += len(pline)

    begin(in_list[0][0][0][0], in_list[0][0][0][1], total_xp + 1)

    for indx, pline in enumerate(in_list):
        down()
        for line in pline:
            draw(line[0][0],line[0][1],line[1][0],line[1][1])

            # можно добавить возможность показывать не только рисунки, но и пробеги (в try), видеть оптимизацию

            # _plot_x_lin.append(line[0][0])
            # _plot_y_lin.append(line[0][1])

            # _plot_x_lin.append(line[1][0])
            # _plot_y_lin.append(line[1][1])

        up()
        try:
            draw(pline[-1][1][0], pline[-1][1][1], in_list[indx+1][0][0][0], in_list[indx+1][0][0][1])
        except IndexError:
            pass
            
    end()

    n_point = 1

    # ax = plt.subplots()[1]
    # # plt.hist('x', orientation=u'horizontal')

    # for i in list(range(len(_plot_xs))):
    #     ax.plot(_plot_xs[i], _plot_ys[i])

    # ax.vlines(280, -155, 155)
    # ax.vlines(480, -155, 155)
    # ax.hlines(-155, 280, 480)
    # ax.hlines(155, 280, 480)

    # ax.set_xlabel('X')
    # ax.set_ylabel('Y')
    # ax.grid()
    # plt.show()

    # _plot_xs = []
    # _plot_ys = []

    return (_dat, _src)

    



if __name__ == '__main__':
    '''
    in_list = [
        [
            [[1, 1], [2, 1]],
            [[2, 1], [3, 1]],
            [[3, 1], [4, 1]]
        ],
        [
            [[1, 2], [2, 2]],
            [[2, 2], [3, 2]],
            [[3, 2], [4, 2]]
        ]
    ]
    '''
    # gen_kuka_code(in_list)

