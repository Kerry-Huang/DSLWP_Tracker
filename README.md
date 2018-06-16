DSLWP_Tracker
==========

Install
----------
(1) git clone https://github.com/Hamlib/Hamlib.git  
(2) ./configure  
(3) make  
(4) sudo make install  
(5) sudo ldconfig  
  
Run  
----------
(1) Download program_tracking_dslwp-b XXXXXXXX.txt  
    <https://github.com/bg2bhc/dslwp_dev>  
(2) edit ./config.ini  
(3) run rotctld  
    example: <sudo rotctld --model=903 --rot-file=/dev/ttyUSB0 --serial-speed=9600 -T 127.0.0.1 -t 4533>  
    see the detail in <http://hamlib.sourceforge.net/pdf/rotctld.8.pdf>  
(3) python track.py  
