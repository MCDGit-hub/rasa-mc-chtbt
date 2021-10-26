# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions import DataConstants
from actions.DocRequirementFinder import DocRequirementFinder
from actions.McdData import McdData

mcd_data = McdData()

class ActionServiceAbout(Action):
    def name(self) -> Text:
        return "action_get_service_about"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        service_name = str(tracker.get_slot("service_type")).upper()

        service_info_dat = mcd_data.get_service_about_data()

        service_fullform = None
        service_info = None

        if(service_name in service_info_dat.keys()):
            service_fullform,service_info = service_info_dat[service_name]['fullform'],\
                                        service_info_dat[service_name]['info'] if service_name in service_info_dat.keys() else None

        if(service_info != None):
            response_msg = "{}:\n{}".format(service_fullform, service_info)
        else:
            response_msg = "Couldn't find {} in our services. Please make sure you have typed the name correctly!".format(service_name)

        dispatcher.utter_message(text=response_msg)

        return []

class ActionGetTradeCategories(Action):
    def name(self) -> Text:
        return "action_get_trade_categories"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        service_name = str(tracker.get_slot("service_type")).upper()

        trade_info_dat = mcd_data.get_trade_category_by_service()

        trade_categories = trade_info_dat[service_name] if service_name in trade_info_dat.keys() else None

        if(trade_categories != None):
            #categories_str = ""
            #idx = 1
            #for category in trade_categories:
            #    categories_str+= str(idx)+". "+category+"\n"
            #    idx+=1
            response_msg = "Following Trade Categories are available in {}:\n:{}".format(service_name, trade_categories)
        else:
            response_msg = "Couldn't find trade categories for {}. Please make sure you have typed the name correctly!".format(service_name)

        dispatcher.utter_message(text=response_msg)

        return []

class ActionGetDocReq(Action):
    # MIGHT BE CORPORATION INFLUENCED
    def name(self) -> Text:
        return "action_get_document_requirements"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        service_name = str(tracker.get_slot("service_type")).upper()
        license_update_type = str(tracker.get_slot("license_update")).upper()
        sub_category = str(tracker.get_slot("sub_category")).upper()

        print(service_name+" : "+license_update_type+" : "+sub_category)

        document_req_data = mcd_data.get_document_info_by_service_and_li_update()

        doc_req_find = DocRequirementFinder()
        response_msg = doc_req_find.find_doc_in_repo(service_name, license_update_type, sub_category, document_req_data)

        print(response_msg)
        dispatcher.utter_message(text=response_msg)

        return []

class ActionGetApplySteps(Action):
    def name(self) -> Text:
        return "action_get_steps_to_apply_licence"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        service_name = str(tracker.get_slot("service_type")).upper()

        service_step_dat = mcd_data.get_steps_to_apply()

        if(service_name in service_step_dat.keys()):
            response_msg = "Please follow the steps below to apply for NEW {} License:\n{}".format(service_name, service_step_dat[service_name])
        else:
             response_msg = "Couldn't find {} in our services. Please make sure you have typed the name correctly!".format(service_name)

        dispatcher.utter_message(text=response_msg)

        return []

class ActionGetApplyStepsAmendmentSurrenderRenewal(Action):
    def name(self) -> Text:
        return "action_get_steps_to_apply_for_amendment_surrender_renewal"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        service_name = str(tracker.get_slot("service_type")).upper()
        license_update_type = str(tracker.get_slot("license_update")).upper()

        service_step_dat = mcd_data.get_amendment_renewal_surrender_process_steps()

        if(service_name in service_step_dat.keys()):
            if(license_update_type in service_step_dat[service_name].keys()):
                response_msg = "Please follow the steps below to apply for {} of License in {}:\n{}".format(license_update_type,service_name,service_step_dat[service_name][license_update_type])
            else:
                response_msg = "Couldn't find {} in License Types. Please make sure you have typed the name correctly!".format(
                    license_update_type)
        else:
            response_msg = "Couldn't find steps for {} of license in {}. Please make sure you have typed the name correctly!".format(service_step_dat[service_name][license_update_type],service_name)

        dispatcher.utter_message(text=response_msg)

        return []

class ActionGetStepsToSubmitDeficiency(Action):
    def name(self) -> Text:
        return "action_get_steps_to_submit_deficiency"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        service_name = str(tracker.get_slot("service_type")).upper()

        service_step_dat = mcd_data.get_steps_to_submit_deficiency()

        if(service_name in service_step_dat.keys()):
            response_msg = "Please follow the steps below to Submit Deficiency in {}:\n{}".format(service_name, service_step_dat[service_name])
        else:
             response_msg = "Couldn't find {} in our services. Please make sure you have typed the name correctly!".format(service_name)

        dispatcher.utter_message(text=response_msg)

        return []

class ActionGetStepsToSearchLegacyRecord(Action):
    def name(self) -> Text:
        return "action_get_steps_to_search_legacy_record"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        service_name = str(tracker.get_slot("service_type")).upper()

        service_step_dat = mcd_data.get_steps_to_search_for_legacy_record()

        if(service_name in service_step_dat.keys()):
            response_msg = "Please follow the steps below to Search for Legacy Record in {}:\n{}".format(service_name, service_step_dat[service_name])
        else:
             response_msg = "Couldn't find {} in our services. Please make sure you have typed the name correctly!".format(service_name)

        dispatcher.utter_message(text=response_msg)

        return []

class ActionFeeInfo(Action):
    # CORPORATION INFLUENCED
    def name(self) -> Text:
        return "action_get_fee_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        service_name = str(tracker.get_slot("service_type")).upper()

        #SDMC example
        if(service_name == "VTL"):
            response_msg = "Click on the link below for Fees & Charges for VTL SDMC.\nLINK: "+DataConstants.vtl_sdmc_fee_structure_link
            dispatcher.utter_message(text=response_msg)
            return []
        else:
            response_msg = "Couldn't find fee & charges for {} in our services. Please make sure you have typed the name correctly!".format(service_name)
            dispatcher.utter_message(text=response_msg)
            return []