# ==================================================================================
#       Copyright (c) 2020 AT&T Intellectual Property.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# ==================================================================================
"""
qpdriver entrypoint module

RMR Messages
 #define TS_UE_LIST 30000
 #define TS_QOE_PRED_REQ 30001
 #define TS_QOE_PREDICTION 30002
30000 is the message type QPD receives; sends out type 30001, which should be routed to QP.
"""

import json
from os import getenv
from ricxappframe.xapp_frame import RMRXapp, rmr
from qpdriver import data
from qpdriver.exceptions import UENotFound


# pylint: disable=invalid-name
rmr_xapp = None


def post_init(self):
    """
    Function that runs when xapp initialization is complete
    """
    self.def_hand_called = 0
    self.traffic_steering_requests = 0


def default_handler(self, summary, sbuf):
    """
    Function that processes messages for which no handler is defined
    """
    self.def_hand_called += 1
    self.logger.warning("QP Driver received an unexpected message of type: {}".format(summary[rmr.RMR_MS_MSG_TYPE]))
    self.rmr_free(sbuf)


def policy_handler(self, summary, sbuf):
    """
    This is the main handler for this xapp, which handles traffic steering requests.
    Traffic steering requests predictions on a set of UEs.
    This app fetches a set of data, merges it together in a deterministic way,
    then sends a new message out to the QP predictor Xapp.
    """
    self.logger.warning("QPD had received A1 Policy!")
    self.logger.warning("Message type of the policy: {}".format(summary[rmr.RMR_MS_MSG_TYPE]))
    self.logger.warning("Policy ID of the policy: {}".format(summary[rmr.RMR_MS_SUB_ID]))
    self.logger.warning("Payload of the Policy: {}".format(summary[rmr.RMR_MS_PAYLOAD]))
    
    self.rmr_free(sbuf)
    
    
    # Access the ue data though SDL
    ue_list = ["257", "258", "259", "260", "261", "262", "264", "265"]

    for ueid in ue_list:
        ue_data_bytes = self.sdl_get("TS-UE-metrics", ueid, usemsgpack=False)
        ue_data = json.loads(ue_data_bytes.decode())
        self.logger.debug("ue data is: {}".format(ue_data))
    
    # Send the fake ue data to QP xApp
    ue_message = { 'ueid-list' : [57,123,224,378,465,578,618,748,859,954], 'ue-data': { '57':{'rsrp': 74, 'rsrq': 65, 'rssinr': 113}, '123':{'rsrp': 45, 'rsrq': 28, 'rssinr': 78}, '224':{'rsrp': 57, 'rsrq': 47, 'rssinr': 89}, '378':{'rsrp': 98, 'rsrq': 83, 'rssinr': 134}, '465':{'rsrp': 85, 'rsrq': 69, 'rssinr': 99}, '578':{'rsrp': 34, 'rsrq': 19, 'rssinr': 59}, '618':{'rsrp': 67, 'rsrq': 46, 'rssinr': 82}, '748':{'rsrp': 36, 'rsrq': 22, 'rssinr': 70}, '859':{'rsrp': 85, 'rsrq': 73, 'rssinr': 134}, '954':{'rsrp': 53, 'rsrq': 36, 'rssinr': 74}  } }
    payload = json.dumps(ue_message).encode()
    success = self.rmr_send(payload, 35000)
    
    if not success:
            self.logger.debug("QP Driver was unable to send to QP!")
    
 
def qp_message_handler(self, summary, sbuf):
    self.logger.warning("QPD had received the qp message!")
    
    self.logger.debug("message handler received message type {}".format(summary[rmr.RMR_MS_MSG_TYPE]))
    self.logger.debug("message is " + summary[rmr.RMR_MS_PAYLOAD].decode())
   
    self.rmr_free(sbuf) 
    
 
def start(thread=False):
    """
    This is a convenience function that allows this xapp to run in Docker
    for "real" (no thread, real SDL), but also easily modified for unit testing
    (e.g., use_fake_sdl). The defaults for this function are for the Dockerized xapp.
    """
    global rmr_xapp
    fake_sdl = getenv("USE_FAKE_SDL", None)
    rmr_xapp = RMRXapp(default_handler, rmr_port=4560, post_init=post_init, use_fake_sdl=bool(fake_sdl))
    rmr_xapp.register_callback(policy_handler, 20010)
    rmr_xapp.register_callback(qp_message_handler , 35001)
    rmr_xapp.run(thread)


def stop():
    """
    can only be called if thread=True when started
    TODO: could we register a signal handler for Docker SIGTERM that calls this?
    """
    rmr_xapp.stop()


def get_stats():
    """
    hacky for now, will evolve
    """
    return {"DefCalled": rmr_xapp.def_hand_called,
            "SteeringRequests": rmr_xapp.traffic_steering_requests}
