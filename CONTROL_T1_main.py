import time
import sys
from PyQt5 import QtWidgets
from main import Ui_Preferences
from myFunct import myFunctions
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog
from checkPorts import CheckPorts
from PyQt5.QtGui import QIcon




class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.check = CheckPorts()
        self.check_p = None
        self.myF = myFunctions()
        self.ser_result = self.myF.serial_ports()
        self.len_o = 0
        self.setWindowIcon(QIcon('LogoT1.png'))
        self.ser = None
        self.textLogin = ['']
        self.textPassword = ['']
        self.Qstr = ''
        self.out = ''
        self.port = ''
        self.wait = 0
        self.connected = False
        self.start_switch = False
        self.switch_interval = True
        self.WiFi_is_connect = bool()
        self.param_loading = False
        self.device_number = 0
        self.ui = Ui_Preferences()
        self.ui.setupUi(self)
        self.setWindowTitle("CONTROL T1")
        self.progress = 0
        self.palette = QtGui.QPalette()
        self.i = 0
        self.But_Slider_1 = ''
        self.But_Slider_2 = ''
        self.But_Slider_3 = ''
        self.MIDI_Chan_Slider = ''
        self.Laten = ''
        self.Dist_min = ''
        self.Dist_max = ''
        self.Smooth = ''
        self.Pot_Left = ''
        self.Pot_Right = ''
        self.S_S_S = ''
        self.LED_P = ''
        self.LED_S = ''
        self.LED_B = ''
        self.But_SS = ''
        self.But_Pots = ''
        self.But_Buttons = ''
        self.ui.SuperSonic.toggled.connect(self.SuperSonic_toggled)
        self.ui.SuperSonic.setToolTip('Enable/Disable Super Sonic Sensor')
        self.ui.Login.textEdited.connect(self.text_Login)
        self.ui.Password.textEdited.connect(self.text_Password)
        self.ui.Connect.clicked.connect(self.Connect)
        self.ui.Connect.setToolTip('Connect and Save WiFi parameters to hardware')
        self.ui.Get_IP.clicked.connect(self.Get_IP)
        self.ui.Get_IP.setToolTip('Get IP Address from hardware')
        self.ui.Buttons.clicked.connect(self.Button_toggled)
        self.ui.Buttons.setToolTip('Enable/Disable Buttons')
        self.ui.Potentiometrs.clicked.connect(self.Potentiometrs_toggled)
        self.ui.Potentiometrs.setToolTip('Enable/Disable Potentiometers')
        self.ui.Distance_min_Slider.valueChanged.connect(self.Distance_min)
        self.ui.Distance_max_Slider.valueChanged.connect(self.Distance_max)
        self.ui.Smooth_Slider.valueChanged.connect(self.Smoothing)
        self.ui.spinBox.valueChanged.connect(self.Buttons_Slider_1)
        self.ui.button_Slider_2.valueChanged.connect(self.Buttons_Slider_2)
        self.ui.button_Slider_3.valueChanged.connect(self.Buttons_Slider_3)
        self.ui.MIDI_Channel_Slider.valueChanged.connect(self.MIDI_Channel_Slider)
        self.ui.Latency_Slider.valueChanged.connect(self.Latency_Slider)
        self.ui.Pot_Left_Slider.valueChanged.connect(self.Potentiometer_Left)
        self.ui.Pot_Right_Slider.valueChanged.connect(self.Potentiometer_Right)
        self.ui.SS_Slider.valueChanged.connect(self.Super_Sonic_Sensor)
        self.ui.LED_Prog_Slider.valueChanged.connect(self.LED_Programm_Slider)
        self.ui.LED_Speed_Slider.valueChanged.connect(self.LED_Speed_Slider)
        self.ui.LED_Bright_Slider.valueChanged.connect(self.LED_Brightness_Slider)
        self.ui.Button_Save.clicked.connect(self.Refresh)
        self.ui.Button_Save.setToolTip('Load and Refresh all Parameters from Device')
        self.ui.Load_Preset.clicked.connect(self.showDialogRead)
        self.ui.Load_Preset.setToolTip('Load Preset from Disk')
        self.ui.Save_Preset.clicked.connect(self.showDialogWrite)
        self.ui.Save_Preset.setToolTip('Save Preset to Disk')
        self.ui.Quit.clicked.connect(self.Quit)
        self.ui.Quit.setToolTip('Exit')
        self.ui.Store.clicked.connect(self.Store_Param)
        self.ui.Store.setToolTip('Store Parameters to Device')
        self.ui.Load_Param_Progress.setVisible(False)
        self.ui.widget_12.setVisible(False)
        self.data_Complicate = list()
        self.device()



    def serialConnect(self):
        try:
            self.ser.close()
            del self.ser
        except:
            pass
        print("ser_res - ")
        print(self.ser_result)
        print('self.device_number => ')
        print(self.device_number)
        self.len_o = len(self.ser_result) - 1
        try:
            self.ser = self.myF.serial_begin(self.ser_result, self.device_number)
            self.ser.isOpen()
        except:
            pass
        QTimer.singleShot(1000, self.Start)

    def device(self):
        if self.connected is False:
            self.ser_result = self.myF.serial_ports()
            check = self.check_Ports()
            print('self.connected =>')
            print(self.connected)
            print('check =>')
            print(check)
            for i in range(len(self.ser_result)):
                if self.ser_result[i] == check:
                    self.device_number = i
                    self.serialConnect()
                    self.connected = True
                    self.ui.WiFi_is_Con.setVisible(True)
                    self.ui.WiFi_is_Con.setText('   Connecting...')
                    break
                elif self.ser_result[i] != check:
                    self.ui.COM_Ports.setText('  NO DEVICE')

        try:
            self.ser.flush()
            QTimer.singleShot(1000, self.device)
        except:
            self.connected = False
            self.start_switch = False
            self.switch_interval = False
            self.param_loading = False
            QTimer.singleShot(10, self.device)
            self.ui.WiFi_is_Con.setHidden(True)
            self.ui.lineEdit_3.clear()
            self.ui.lineEdit_4.clear()




    def Start(self):
        self.out = ''
        self.switch_interval = False

        if self.param_loading is False:
            try:
                self.ser.write('__CHECK_DEV__'.encode('utf_8') + b'\n')
                time.sleep(0.1)
                self.ser.flush()
                self.ser.write(' '.encode('utf_8') + b'\n')
                time.sleep(0.1)
                self.ser.flush()

            except:
                print('AAAAAAA')
                QTimer.singleShot(1000, self.device)
                self.connected = False
                self.start_switch = False
                self.switch_interval = False
                self.param_loading = False

        if self.start_switch is False:

            try:
                while self.ser.inWaiting() > 0:
                    self.out += self.ser.read(1).decode()
                    out = self.out.split('\r\n')
                    print('out => ')
                    print(out[0])
                    print('self.wait =>')
                    print(self.wait)
                    for i in range(len(out)-1):
                        print('out => ')
                        print(out[i])
                        if out[i] == 'CONTROL_T1':
                            self.start_switch = True
                            self.ui.COM_Ports.setText('CONTROL T1')
                            self.ui.WiFi_is_Con.setVisible(True)
                            QTimer.singleShot(1500, self.Refresh)
                            QTimer.singleShot(2000, self.Interval)
                            self.layout().update()
                            self.Get_IP()

                        elif out[i] == 'CONTROL_A1':
                            self.wait += 1
                            self.check.switchChange()
                            self.param_loading = False
                            self.connected = False
                            self.switch_interval = False
                            self.start_switch = False
                            self.device()
                            self.wait += 1

                        elif out[i] != 'CONTROL_T1' and (self.wait % 10) == 0:
                            self.wait += 1
                            self.check.switchChange()
                            self.param_loading = False
                            self.connected = False
                            self.switch_interval = False
                            self.start_switch = False
                            self.device()
                            break

                        elif self.out != 'CONTROL_T1':
                             self.ui.WiFi_is_Con.setHidden(True)
                             self.start_switch = False
                             self.wait += 1
                else:
                    QTimer.singleShot(1000, self.Start)

            except:
                QTimer.singleShot(1000, self.Start)

    def Refresh(self):
        self.ui.Load_Param.setVisible(True)
        time.sleep(0.05)
        if self.WiFi_is_connect is True:
            try:
                self.ser.write('__Refresh__'.encode('utf_8') + b'\n')
            except:
                pass
            time.sleep(0.05)
            self.Send_Dump()
            self.Update()







    def Update(self):
        self.ui.Load_Param.setHidden(True)
        self.ui.Load_Param_Progress.setHidden(True)
        self.ui.widget_12.setHidden(True)
        print('param_loading => ')
        print(self.param_loading)
        if self.param_loading is False:
            self.ui.WiFi_is_Con.setVisible(True)
            self.ui.WiFi_is_Con.setText('      Loading...')
        else:
            self.ui.WiFi_is_Con.setVisible(False)
        if self.WiFi_is_connect is True and self.param_loading is True:
            self.ui.WiFi_is_Con.setVisible(True)
            self.ui.WiFi_is_Con.setText('WiFi Connected')
        self.layout().update()
        QTimer.singleShot(2000, self.Interval)

    def Send_Dump(self):
        self.switch_interval = False
        self.start_switch = False

        try:
            self.out = ''
            self.ser.flushInput()
            self.ser.flushOutput()
            time.sleep(0.05)
            self.ser.write('__SEND_D__'.encode('utf_8') + b'\n')
            print('__SEND_D__')
            QTimer.singleShot(10, self.getParam)
        except:
            QTimer.singleShot(1200, self.Refresh)

    def getParam(self):
        while self.ser.inWaiting() > 0:
                self.out += self.ser.read(1).decode()
        print('GET PARAM')
        self.Param_Loading()


    def Param_Loading(self):

        res1 = self.out.split('\r\n')
        try:
            for i in range(len(res1)-1):
                a = res1[i]
                if a == 'WiFi Connected!':
                    del res1[i]
                elif a == 'CONTROL_T1':
                    del res1[i]
                elif a == ' ':
                    del res1[i]
                elif a == '0.0.0.0':
                    del res1[i]
            print('res1 =>')
            print(res1)

            self.ui.SuperSonic.setChecked(self.str2bool(res1[0]))
            self.ui.Potentiometrs.setChecked(self.str2bool(res1[1]))
            self.ui.Buttons.setChecked(self.str2bool(res1[2]))
            self.ui.Latency_Slider.setValue(int(res1[3]))
            self.ui.button_Slider_1.setValue(int(res1[4]))
            self.ui.button_Slider_2.setValue(int(res1[5]))
            self.ui.button_Slider_3.setValue(int(res1[6]))
            self.ui.Distance_min_Slider.setValue(int(res1[7]))
            self.ui.Distance_max_Slider.setValue(int(res1[8]))
            self.ui.Smooth_Slider.setValue(int(res1[9]))
            self.ui.Pot_Left_Slider.setValue(int(res1[10]))
            self.ui.Pot_Right_Slider.setValue(int(res1[11]))
            self.ui.SS_Slider.setValue(int(res1[12]))
            self.ui.LED_Prog_Slider.setValue(int(res1[13]))
            self.ui.LED_Speed_Slider.setValue(int(float(res1[14])))
            self.ui.LED_Bright_Slider.setValue(int(res1[15]))
            self.ui.MIDI_Channel_Slider.setValue(int(res1[16]))

            self.ui.WiFi_is_Con.setText('     Done')
            time.sleep(1)
            self.switch_interval = True
            self.param_loading = True
            self.start_switch = True
            self.layout().update()


        except:
            self.param_loading = False
            if self.WiFi_is_connect:
                QTimer.singleShot(200, self.Send_Dump)
            else:
                pass






    def showDialogRead(self):

        fname = QFileDialog.getOpenFileName(self, 'Open file', '')[0]
        try:
            f = open(fname, 'r')

            with f:
                d = f.read()
                data = d.split('\n')
                self.But_Slider_1 = data[0]
                self.But_Slider_2 = data[1]
                self.But_Slider_3 = data[2]
                self.MIDI_Chan_Slider = data[3]
                self.Laten = data[4]
                self.Dist_min = data[5]
                self.Dist_max = data[6]
                self.Smooth = data[7]
                self.Pot_Left = data[8]
                self.Pot_Right = data[9]
                self.S_S_S = data[10]
                self.LED_P = data[11]
                self.LED_S = data[12]
                self.LED_B = data[13]
                self.But_SS = data[14]
                self.But_Pots = data[15]
                self.But_Buttons = data[16]
            QTimer.singleShot(10, self.Store_Param)
            QTimer.singleShot(10, self.Refresh)
        except FileNotFoundError:
            pass



    def showDialogWrite(self):

        fname = QFileDialog.getSaveFileName(self, 'Save file', '')[0]
        self.dataComplicate()
        del_ = fname.split('.')
        try:
            f = open(del_[0] + '.t1', 'w')
            for index in range(len(self.data_Complicate)):
                f.write(self.data_Complicate[index] + '\n')

            f.close()
        except:
            pass

    def dataComplicate(self):

        self.data_Complicate = [self.But_Slider_1,
                                self.But_Slider_2,
                                self.But_Slider_3,
                                self.MIDI_Chan_Slider,
                                self.Laten,
                                self.Dist_min,
                                self.Dist_max,
                                self.Smooth,
                                self.Pot_Left,
                                self.Pot_Right,
                                self.S_S_S,
                                self.LED_P,
                                self.LED_S,
                                self.LED_B,
                                self.But_SS,
                                self.But_Pots,
                                self.But_Buttons
                                ]



    def Interval(self):
        if self.switch_interval is True:
            out = ['']
            self.i = self.i + 1
            self.out = ''
            self.ui.Load_Param_Progress.setValue(self.progress)
            try:
                self.ser.write('__RECIVE_D__'.encode('utf_8') + b'\n')
                time.sleep(0.3)
                QTimer.singleShot(10000, self.Interval)
                while self.ser.inWaiting() > 0:
                    self.out += self.ser.read(1).decode()
                    out = self.out.split('\r\n')
                for i in range(len(out)-1):
                    if out[i] == 'WiFi':
                        self.ui.WiFi_is_Con.setVisible(True)
                        self.ui.WiFi_is_Con.setText('WiFi Connected')
                    elif out[i] == '!WiFi':
                        self.ui.WiFi_is_Con.setVisible(True)
                        self.ui.WiFi_is_Con.setText('WiFi not connected')
                        self.ui.lineEdit_3.clear()
                        self.ui.lineEdit_4.clear()

                    else:
                        self.ui.WiFi_is_Con.setHidden(True)

                self.layout().update()
            except:
                QTimer.singleShot(10000, self.Interval)
        else:
            QTimer.singleShot(10000, self.Interval)







    @pyqtSlot()

    def Get_IP(self):
        out = ''
        a = ''
        try:
            self.ser.flushInput()
            self.ser.flushOutput()
            self.ui.lineEdit_3.clear()
            self.ui.lineEdit_4.clear()
            self.ser.write('__Get_IP__'.encode('utf_8') + b'\n')
            time.sleep(0.1)
            while self.ser.inWaiting() > 0:
                out += self.ser.read(1).decode()
            a = out.split('\r\n')
            self.ui.lineEdit_3.setText(a[len(a)-2])
            self.ui.lineEdit_4.setText('5004')
            split = a[len(a) - 2].split('.')
            if split[1] == '0':
                self.WiFi_is_connect = False
                self.WiFi_is_now_connect = False
                self.ui.WiFi_is_Con.setVisible(True)
                self.ui.WiFi_is_Con.setText('WiFi not Connected')

            if split[0] == '192':
                self.WiFi_is_connect = True
                self.WiFi_is_now_connect = True

        except:
            QTimer.singleShot(1200, self.Get_IP)




    def Connect(self):
        a = 0.2
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write('__Log__'.encode('utf_8') + b'\n')
        self.ser.flush()
        time.sleep(a)
        self.ser.write(bytes(self.textLogin[len(self.textLogin) - 1].encode('utf_8') + b'\n'))
        self.ser.flush()
        time.sleep(a)
        self.ser.write('__Pass__'.encode('utf_8') + b'\n')
        time.sleep(a)
        self.ser.write(bytes(self.textPassword[len(self.textPassword) - 1].encode('utf_8') + b'\n'))
        self.ser.flush()
        time.sleep(a)
        self.ser.write('__Refresh__'.encode('utf_8') + b'\n')
        time.sleep(a)
        self.ui.WiFi_is_Con.setVisible(False)
        self.ui.Login.setText('***********')
        self.ui.Password.setText('***********')
        self.ser.flushInput()
        self.ser.flushOutput()



    def text_Login(self, QString):
       for i in range(len(QString)):
            self.textLogin = [QString]

    def text_Password(self, QString):
       for i in range(len(QString)):
            self.textPassword = [QString]


    def Store_Param(self):
        a = 0.1
        try:
            self.ser.write('__Dist_min__'.encode('utf_8') + b'\n')
            time.sleep(a)
            self.ser.write(self.Dist_min.encode('utf_8') + b'\n')
            time.sleep(a)
            self.ser.write('__Dist_max__'.encode('utf_8') + b'\n')
            time.sleep(a)
            self.ser.write(self.Dist_max.encode('utf_8') + b'\n')
            time.sleep(a)
            self.ser.write('__Smooth__'.encode('utf_8') + b'\n')
            time.sleep(a)
            self.ser.write(self.Smooth.encode('utf_8') + b'\n')
            time.sleep(a)
            self.ser.write('__P1_b1_on__'.encode('utf_8') + b'\n')
            time.sleep(a)
            self.ser.write(self.But_Slider_1.encode('utf_8') + b'\n')
            time.sleep(a)
            self.ser.write('__P2_b2_on__'.encode('utf_8') + b'\n')
            time.sleep(a)
            self.ser.write(self.But_Slider_2.encode('utf_8') + b'\n')
            time.sleep(a)
            self.ser.write('__P3_b3_on__'.encode('utf_8') + b'\n')
            time.sleep(a)
            self.ser.write(self.But_Slider_3.encode('utf_8') + b'\n')
            time.sleep(a+0.5)
            self.ser.write('__MIDI_chan__'.encode('utf_8') + b'\n')
            time.sleep(a)
            self.ser.write(self.MIDI_Chan_Slider.encode('utf_8') + b'\n')
            time.sleep(a)
            self.ser.write('__Latency__'.encode('utf_8') + b'\n')
            time.sleep(a)
            self.ser.write(self.Laten.encode('utf_8') + b'\n')
            time.sleep(a)
            self.ser.write('__Pot_L__'.encode('utf_8') + b'\n')
            time.sleep(a)
            self.ser.write(self.Pot_Left.encode('utf_8') + b'\n')
            time.sleep(a)
            self.ser.write('__Pot_R__'.encode('utf_8') + b'\n')
            time.sleep(a)
            self.ser.write(self.Pot_Right.encode('utf_8') + b'\n')
            time.sleep(a)
            self.ser.write('__S_S_S__'.encode('utf_8') + b'\n')
            time.sleep(a)
            self.ser.write(self.S_S_S.encode('utf_8') + b'\n')
            time.sleep(a+0.5)
            self.ser.write('__L_P__'.encode('utf_8') + b'\n')
            time.sleep(a)
            self.ser.write(self.LED_P.encode('utf_8') + b'\n')
            time.sleep(a)
            self.ser.write('__L_S__'.encode('utf_8') + b'\n')
            time.sleep(a)
            self.ser.write(self.LED_S.encode('utf_8') + b'\n')
            time.sleep(a)
            self.ser.write('__L_B__'.encode('utf_8') + b'\n')
            time.sleep(a)
            self.ser.write(self.LED_B.encode('utf_8') + b'\n')
            time.sleep(a)
            if self.But_SS == '0':
                self.ser.write('__SSB_off__'.encode('utf_8') + b'\n')
            else:
                self.ser.write('__SSB_on__'.encode('utf_8') + b'\n')
            time.sleep(a)
            if self.But_SS == '0':
                self.ser.write('__Pot_off__'.encode('utf_8') + b'\n')
            else:
                self.ser.write('__Pot_on__'.encode('utf_8') + b'\n')
            time.sleep(a)
            if self.But_SS == '0':
                self.ser.write('__But_off__'.encode('utf_8') + b'\n')
            else:
                self.ser.write('__But_on__'.encode('utf_8') + b'\n')

            self.ser.write('__SAVE__'.encode('utf_8') + b'\n')
        except:
            print('ALARM')


    def Distance_min(self, QString):
        try:
            self.Qstr = str(QString)
            self.Dist_min = self.Qstr
            self.ser.write('__Dist_min__'.encode('utf_8') + b'\n')
            time.sleep(0.01)
            self.ser.write(self.Qstr.encode('utf_8') + b'\n')
            time.sleep(0.05)
        except:
            pass

    def Distance_max(self, QString):
        try:
            self.Qstr = str(QString)
            self.Dist_max = self.Qstr
            self.ser.write('__Dist_max__'.encode('utf_8') + b'\n')
            time.sleep(0.01)
            self.ser.write(self.Qstr.encode('utf_8') + b'\n')
            time.sleep(0.05)
        except:
            pass

    def Smoothing(self, QString):
        try:
            self.Qstr = str(QString)
            self.Smooth = self.Qstr
            self.ser.write('__Smooth__'.encode('utf_8') + b'\n')
            time.sleep(0.01)
            self.ser.write(self.Qstr.encode('utf_8') + b'\n')
            time.sleep(0.05)
        except:
            pass

    def Buttons_Slider_1(self, QString):
        try:
            self.Qstr = str(QString)
            self.But_Slider_1 = self.Qstr
            self. ser.write('__P1_b1_on__'.encode('utf_8') + b'\n')
            time.sleep(0.01)
            self.ser.write(self.Qstr.encode('utf_8') + b'\n')
            time.sleep(0.05)
        except:
            pass

    def Buttons_Slider_2(self, QString):
        try:
            self.Qstr = str(QString)
            self.But_Slider_2 = self.Qstr
            self.ser.write('__P2_b2_on__'.encode('utf_8') + b'\n')
            time.sleep(0.01)
            self.ser.write(self.Qstr.encode('utf_8') +  b'\n')
            time.sleep(0.05)
        except:
            pass

    def Buttons_Slider_3(self, QString):
        try:
            self.Qstr = str(QString)
            self.But_Slider_3 = self.Qstr
            self.ser.write('__P3_b3_on__'.encode('utf_8') + b'\n')
            time.sleep(0.01)
            self.ser.write(self.Qstr.encode('utf_8') + b'\n')
            time.sleep(0.05)
        except:
            pass

    def MIDI_Channel_Slider(self, QString):
        try:
            self.Qstr = str(QString)
            self.MIDI_Chan_Slider = self.Qstr
            self.ser.write('__MIDI_chan__'.encode('utf_8') + b'\n')
            time.sleep(0.01)
            self.ser.write(self.Qstr.encode('utf_8') + b'\n')
            time.sleep(0.05)
        except:
            pass

    def Latency_Slider(self, QString):
        try:
            self.Qstr = str(QString)
            self.Laten = self.Qstr
            self.ser.write('__Latency__'.encode('utf_8') + b'\n')
            time.sleep(0.01)
            self.ser.write(self.Qstr.encode('utf_8') + b'\n')
            time.sleep(0.05)
        except:
            pass

    def Potentiometer_Left(self, QString):
        try:
            self.Qstr = str(QString)
            self.Pot_Left = self.Qstr
            self.ser.write('__Pot_L__'.encode('utf_8') + b'\n')
            time.sleep(0.01)
            self.ser.write(self.Qstr.encode('utf_8') + b'\n')
            time.sleep(0.05)
        except:
            pass

    def Potentiometer_Right(self, QString):
        try:
            self.Qstr = str(QString)
            self.Pot_Right = self.Qstr
            self.ser.write('__Pot_R__'.encode('utf_8') + b'\n')
            time.sleep(0.01)
            self.ser.write(self.Qstr.encode('utf_8') + b'\n')
            time.sleep(0.05)
        except:
            pass

    def Super_Sonic_Sensor(self, QString):
        try:
            self.Qstr = str(QString)
            self.S_S_S = self.Qstr
            self.ser.write('__S_S_S__'.encode('utf_8') + b'\n')
            time.sleep(0.01)
            self.ser.write(self.Qstr.encode('utf_8') + b'\n')
            time.sleep(0.05)
        except:
            pass

    def LED_Programm_Slider(self, QString):
        try:
            self.Qstr = str(QString)
            self.LED_P = self.Qstr
            self.ser.write('__L_P__'.encode('utf_8') + b'\n')
            time.sleep(0.01)
            self.ser.write(self.Qstr.encode('utf_8') + b'\n')
            time.sleep(0.05)
        except:
            pass

    def LED_Speed_Slider(self, QString):
        try:
            self.Qstr = str(QString)
            self.LED_S = self.Qstr
            self.ser.write('__L_S__'.encode('utf_8') + b'\n')
            time.sleep(0.01)
            self.ser.write(self.Qstr.encode('utf_8') + b'\n')
            time.sleep(0.05)
        except:
            pass

    def LED_Brightness_Slider(self, QString):
        try:
            self.Qstr = str(QString)
            self.LED_B = self.Qstr
            self.ser.write('__L_B__'.encode('utf_8') + b'\n')
            time.sleep(0.01)
            self.ser.write(self.Qstr.encode('utf_8') + b'\n')
            time.sleep(0.05)
        except:
            pass

    def SuperSonic_toggled(self, checked):
        self.But_SS = self.bool2str(checked)
        try:
            if checked is True:
                self. ser.write('__SSB_on__'.encode('utf_8') + b'\n')
                self.rowOverride = True
            elif checked is False:
                self.ser.write('__SSB_off__'.encode('utf_8') + b'\n')
                self.rowOverride = False
        except:
            pass

    def Potentiometrs_toggled(self, checked):
        self.But_Pots = self.bool2str(checked)
        try:
            if checked is True:
                self.ser.write('__Pot_on__'.encode('utf_8') + b'\n')
                self.rowOverride = True
            elif checked is False:
                self.ser.write('__Pot_off__'.encode('utf_8') + b'\n')
                self.rowOverride = False
        except:
            pass

    def Button_toggled(self, checked):
        self.But_Buttons = self.bool2str(checked)
        try:
            if checked is True:
                self.ser.write('__But_on__'.encode('utf_8') + b'\n')
                self.rowOverride = True
            elif checked is False:
                self.ser.write('__But_off__'.encode('utf_8') + b'\n')
                self.rowOverride = False
        except:
            pass

    def check_Ports(self):
        check_p = self.check.checkPorts()
        return check_p

    def str2bool(self, v):
        return v.lower() in ("yes", "true", "t", "1")

    def bool2str(self, v):
        if v:
            return '1'
        else:
            return '0'


    def Quit(self):
        try:
            self.ser.close()
        except:
            pass
        sys.exit()

