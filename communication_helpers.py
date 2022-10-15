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
        ret_str = []
        x = CommunicationHelper.vcp.read()
        if x == None:
            return []

        str_recv = x.decode('utf-8')

        
        for message in str_recv.split('?'):
            full_message = CommunicationHelper.recv_buffer+message
            CommunicationHelper.recv_buffer = ""
            
            ret_str.append(full_message)

        CommunicationHelper.recv_buffer = ret_str.pop()


        ret = []
        for s in ret_str:
            try:
                data = json.loads(s)
                ret.append(data)
            except:
                pass #TODO
        
        return ret
        """if x.decode('utf_8') == '?':
            ret = dict()
            try:
                ret = json.loads(CommunicationHelper.recv_buffer)
            except:
                ret["error_string"] = CommunicationHelper.recv_buffer
            CommunicationHelper.recv_buffer = ""
            return ret
        else:
            CommunicationHelper.recv_buffer = CommunicationHelper.recv_buffer+x.decode('utf-8')"""
