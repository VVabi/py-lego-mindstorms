import gc
import micropython
import json
import hub

class CommunicationHelper:
    vcp = hub.USB_VCP()

    def is_connected():
        return CommunicationHelper.vcp.isconnected()

    def write_dict_to_serial(data_dict):
       st = json.dumps(data_dict)+"\n\r"
       CommunicationHelper.vcp.write(st)


    recv_buffer = ""
   

    def receive_json_from_serial():
       while True:
           x = CommunicationHelper.vcp.read(1)
           if x == None:
               break
           if x.decode('utf_8') == '?':
               ret = dict()
               try:
                    ret = json.loads(CommunicationHelper.recv_buffer)
               except:
                    ret["error_string"] = CommunicationHelper.recv_buffer
               CommunicationHelper.recv_buffer = ""
               return ret
           else:
               CommunicationHelper.recv_buffer = CommunicationHelper.recv_buffer+x.decode('utf-8')
       return None