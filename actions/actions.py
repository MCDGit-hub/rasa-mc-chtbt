# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import re
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import re

class ActionServiceAbout(Action):
    def name(self) -> Text:
        return "action_get_service_about"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        service_name = str(tracker.get_slot("service_type")).upper()

        service_about_data = {
            'GTL': {'fullform': 'Gen. Trade / Storage License',
                    'info': 'The Central Licensing & Enforcement Cell (CL&EC), SDMC at deals with the issue and renewal of Municipal General Trade/Storage Licenses under the provisions of Section 417 of DMC Act-1957 (amended Time to Time) and composition of offences u/s 469.\nThe Powers of Commissioner for grant of trade/storage license/permission already stand delegated to Dy. Commissioners/ Addl. Dy.\nCommissioner CL&EC u/s 491 of DMC Act.'
                            '\nSection 417 of the DMC Act-1957 (amended time to time) provides that any person, who desires to establish business of a General Trade and Storage, is required to obtain license from SDMC, particularly for the articles mentioned under Part-I & Part-II of the Eleventh Schedule and other articles notified by the Government Authorities by issuing Public Notices/Orders/Directions from time to time.'
                            '\nThe applicant can apply for the same online through the internet or at any of the CSB center at four zonal offices of SDMC.'
                            '\n\n Please Redirect to: https://mcdonline.nic.in/gtlsdmc/web/citizen/info to apply.'},

            'HTL': {'fullform': 'Health License',
                    'info': 'In this service you can apply for Health License.\nPlease redirect to this link: https://mcdonline.nic.in/citizensdmc/web/citizen/info to apply.'},
            'FTL': {'fullform': 'Factory License',
                    'info': 'Section  416  of  the  MCD  Act,  1957  places  an  obligation  power  to  obtain  prior  permission  of'
                            'Commissioner  MCD  in  writing  on  the  person  desirous  to  establish  in  any  premises  or '
                            'materially  alter,  enlarge  or  extend  any  factory,  workshop  or  trade  premises  in  which  it  is '
                            'intended to employ, steam, electricity, water or other mechanical. '
                            'Once the permission is granted under this Section to install some machinery in a premise, it is '
                            'also an obligatory to obtain a trade license as laid down under Section 417 (i) before starting '
                            'the trade. In order to streamline the smooth and orderly growth of industries as per provisions '
                            'of DMC Act, 1957, the Master Plan of Delhi & Pollution Control Committee, G.N.C.T.D., and '
                            'as  per  directions/judgements  delivered  by  the  Supreme  Court  of  India,  the  provisions  are '
                            'implemented in the NCT of Delhi to minimize the nuisance, health hazard and pollution for '
                            'the orderly industrial growth in the NCT of Delhi. In order to achieve this, certain restrictions '
                            'are imposed in form of licensing conditions for different categories of licenses. \nPlease redirect to this link: https://mcdonline.nic.in/ftlsdmc/web/citizen/info to apply'},
            'VTL': {'fullform': 'Veterinary License',
                    'info': 'Veterinary department deals with wide sphere of work such as Issuance of Licenses of Horse '
                            'Buggies, Dairies, Meat Shops, Meat processing units etc. '
                            'This document covers all the important details of the Veterinary Trade License Application '
                            'like Application features, Interfaces, Functional and Non-Functional requirements, Forms '
                            'and its logical validations.\n\n Please redirect to this link: https://mcdonline.nic.in/vtlsdmc/web/citizen/info to apply.'}
        }

        service_info_dat = service_about_data


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

        trade_category_by_service = {
            'GTL': [
                'Conforming industrial area / Flatted group industries and newly Notified 22 areas of industrial area',
                'C.B.D/ sub-C.B.D /Metropolitan city center',
                'Local commercial',
                'LSC (Local Shopping Complex)',
                'CSC (Commercial Shopping Complex)',
                'Community centers',
                'District centers',
                'Service market/ Service center',
                'Pedestrian shopping streets',
                'Commercial areas',
                'Industrial units / plots abutting 24 m row and above in approved layout plan and approved use in sanctions building plan',
                'MLU (mixed land use)',
                'Special area category (old city and its extensions)',
                'Urban/ Rural villages (only in extended Lal Dora Abadi)',
                'Other categories (small shops upto 20 sqm at ground floor in residential area)'],
            'VTL': ['Cattle Dairy Farm', 'Meat Shop', 'Meat Processing Unit', 'Horse Buggy'],
            'FTL': ['Conforming (Industrial) Area', 'DDA/DSIDC/DI Built-up auction/allotted sheds',
                    'Industries Outside Industrial Area', 'Household Category', 'Local Commercial Category'],
            'HTL': ['NOT ANY']
        }

        #trade_info_dat = mcd_data.get_trade_category_by_service()

        trade_categories = trade_category_by_service[service_name] if service_name in trade_category_by_service.keys() else None

        if(trade_categories != None):
            categories_str = ""
            idx = 1
            for category in trade_categories:
                categories_str+= str(idx)+". "+category+"\n"
                idx+=1
            response_msg = "Following Trade Categories are available in {}:\n{}".format(service_name, categories_str)
        else:
            response_msg = "Couldn't find trade categories for {}. Please make sure you have typed the name correctly!".format(service_name)

        dispatcher.utter_message(text=response_msg)

        return []

class ActionGetDocReq(Action):
    def name(self) -> Text:
        return "action_get_document_requirements"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        service_name = str(tracker.get_slot("service_type")).upper()
        license_update_type = str(tracker.get_slot("license_update")).upper()
        sub_category = str(tracker.get_slot("sub_category")).upper()

        print(service_name+" : "+license_update_type+" : "+sub_category)

        document_req_by_service = {
            'GTL': {'NEW': [
                'Proof of legal occupancy of the establishment or allotment letter of govt. agency/tenancy proof/ electricity/water connection bill/landline telephone bill/lease deed /sale deed/GPA.',
                'Id proof (with photograph) i.e. Aadhar card/voter id/ pan card/ valid Indian passport/ permanent driving license, bank pass book with photograph and signature.',
                'Photograph of the establishment with front-facia, display of goods traded from the premises or the business being carried out from the premises.',
                'Site plan/key plan showing the area under the occupation of the applicant or earmarking salient features of the neighbourhood of the site.'],
                'RENEWAL': ['Self attested scanned copy of original GT/SL.',
                            'Self attested scanned copy of last receipt of license fee.',
                            'ID Proof (with photograph) i.e. Aadhar Card/Voter ID/ PAN Card/ Valid Indian Passport/ Permanent driving license, Bank pass book with photograph and signature.'],
                'AMENDMENT': ['Affidavit by the applicant.',
                              'Board Resolution/ MOA / Partnership deed.',
                              'Photograph of site.',
                              'Lease deed /Rent agreement/layout plan.'],
                'SURRENDER': ['UID', 'Undertaking', 'Last receipt of payment']},
            'VTL': {'MEAT SHOP': {'NEW': [
                'Document  regarding  Age  proof  and  ID  proof)  with photograph i.e. Aadhar Card/ Passport/ Driving License/ Voter ID card/ PAN Card. *In case of non-availability of Age proof, the applicant may submit an undertaking in the form of affidavit regarding his/her age proof.(Mandatory)',
                'Proof of legal occupancy of the establishment or allotment letter of Govt.agency / tenancy proof(rent agreement) / latest paid bill of electricity / DJB / Landline phone / Lease deed / Sale deed / GPA.(Mandatory)',
                'Blue  Print, Site Plan showing the inside dimension.(Mandatory)',
                'Proof  of  water  supply/connection  i.e. current water bill and in case of bore well water testing report.(Mandatory)',
                'Medical Fitness certificate issued by authorized registered medical practitioner (MBBS) certifying that the applicant is free form any infectious and contagious disease.(Mandatory)',
                'NOC  from  the  Managing  Committee and or Imam of the Masjid if license is applied for shop situated in compound/building of a Masjid (Mosque).',
                'Conditional- (If Meat shop exist in Masjid premises)Proof of Electricity supply/connection i.e. current Bill. (For NDMC and EDMC) (Mandatory) *not required for SDMC.',
                'Miscellaneous (NM) NDMC '],
                'RENEWAL': [
                    'Medical  Fitness  certificate  issued  by  authorized registered medical practitioner (MBBS) certifying that the applicant is free from any infectious and contagious disease.(Mandatory)',
                    'Residential Address proof (*Conditional-  In  case  of  modification/change in address of applicant).',
                    'Proof of legal occupancy of the establishment or allotment letter of Govt. agency/tenancy proof/latest paid bill of electricity/DJB/Landline phone/Lease deed/Sale deed/GPA. (*Conditional- in case of modification/ change in occupancy)',
                    'Proof of water supply/connection i.e. current water bill and in case of bore well water testing report. (Conditional- if source of water changed).',
                    'Proof which certifies that drainage system changed. (Conditional- if drainage system changed).',
                    'Copy of Old License (Non Mandatory).',
                    'Proof of Last paid receipt of Renewal License fee. (Mandatory).',
                    'Miscellaneous (NM) NDMC'],
                'AMENDMENT': ['Owner/Licensee Photo. (Mandatory).',
                              'Death Certificate of the license holder. Conditional- in case of change of owner.',
                              'Certificate of the legal heirs of the deceased license holder. Conditional- in case of change of owner.',
                              'NoC from rest of the legal heirs in the form of affidavit to transfer the license in the name of the one legal heirs. (Conditional- in case of change of owner.).',
                              'Medical Fitness certificate issued by authorized registered medical practitioner (MBBS) certifying that the applicant is free form any infectious and contagious disease. (Mandatory)',
                              'Proof of change of constitution. (Conditional)',
                              'Proof of addition/deletion of partners in case of change in Partnership. (Conditional)',
                              'Proof of legal occupancy of the establishment or allotment letter of Govt. agency/tenancy proof (rent agreement)/Lease deed/Sale deed/GPA. (Conditional- in case change in Type of Occupancy)',
                              'Miscellaneous (NM) NDMC'],
                'SURRENDER': ['Applicant Identity Proof. (Mandatory)',
                              'Miscellaneous (NM) NDMC']},
                'CATTLE DAIRY FARM': {
                    'NEW': ['Certificate from SDM for verification of Rural Area (For Rural Area)',
                            'Proof of legal occupancy of the establishment or allotment letter of Govt. agency/tenancy proof (rent agreement)/Lease deed/Sale deed/GPA. (Mandatory)',
                            'Document regarding Age proof and Address proof with photograph i.e. Virtual Aadhar Card/ Passport / Driving License/ Voter ID card. (Mandatory)',
                            'Blue print, Site Plan and key plan showing the inside dimension i.e. Length, Width & Height of Cattle Shed/Dairy. (Mandatory)',
                            'Proof of Electricity supply/connection to the cattle shed/ dairy Plot i.e. current Electricity Bill. (Mandatory)',
                            'Proof of water  supply/connection i.e. current water bill and in case of bore well water testing report. (Mandatory)',
                            'NOC from the owner of the property to run Dairy Cattle. (Conditional in case of tenancy). (Based)',
                            'Copy of receipt of latest payment of license fee/ Miltch tax. (Conditional  for  Rural  and  Authorized Dairy)',
                            'Consent form DPCC to operate Dairy (Non Mandatory)',
                            'Proof of Temple is registered with Trust/organization. (Conditional- In case of temple)'],
                    'RENEWAL': [
                        'Address proof (* in case of modification/change in address of applicant). Conditional based.',
                        'Proof of legal occupancy of the establishment or allotment letter of Govt. agency/tenancy proof (rent agreement)/Lease deed/Sale deed/GPA. (Conditional-  in case of change of ownership)',
                        'Copy of receipt of latest payment of license fee/ Miltch tax. (Conditional for Authorized Dairy) (Mandatory)',
                        'Copy of Old License.',
                        'Copy of receipt of latest payment of license fee/ Miltch tax. (Conditional for Rural and Authorized Dairy)',
                    ],
                    'AMENDMENT': ['Owner/Licensee Photo (Mandatory)',
                                  'Death Certificate of the license holder. Conditional- in case of change of owner.',
                                  'Certificate of the legal heirs of the deceased license holder. Conditional- in case of change of owner.',
                                  'NoC from rest of the legal heirs in the form of affidavit to transfer the license in the name of the one legal heirs. Conditional- in case of change of owner.',
                                  'Proof of change of constitution. (conditional).',
                                  'Proof of addition/deletion of partners n case of change in Partnership. Conditional- in case of change in details of partners.',
                                  'Proof of legal occupancy of the establishment or allotment letter of Govt. agency/tenancy proof (rent agreement)/Lease deed/Sale deed/GPA. (Conditional)',
                                  ],
                    'SURRENDER': ['Applicant Identity Proof.']},
                'MEAT PROCESSING UNIT': {
                    'NEW': ['Valid copy of Factory License (Mandatory) VTL-016 – Common for all three corporation.',
                            'Valid copy of Health Trade License (Mandatory) (SDMC).',
                            'Document regarding Age proof and ID proof) with photograph i.e. Aadhar Card/Passport/Driving License/Voter ID card/PAN Card/ any other proof issued by the Govt. Body.(M) Common for all three corporation.',
                            'Proof of ownership/ occupancy of the establishment or allotment letter of Govt. agency/tenancy proof (rent agreement)/Lease deed/Sale deed/GPA. (M) (SDMC).',
                            'Blue  print, Site Plan and key plan showing the inside dimension i.e. Length, Width & Height of establishment. (M) Common for all three corporation',
                            'Proof of water supply/connection i.e. current water bill and in case of bore well water testing report. (M) Common for all three corporation.',
                            'Miscellaneous (NDMC)',
                            'Medical Fitness certificate issued by authorized registered medical practitioner (MBBS) certifying that the applicant and meat handler are free form any infectious and contagious disease. (M) (VTL031) (MPU) (NDMC)',
                            ],
                    'RENEWAL': [
                        'Medical Fitness certificate issued by authorized registered medical practitioner (MBBS) certifying that the applicant and meat handler are free from any infectious and contagious disease. (M) (VTL031) (MPU) (NDMC)',
                        'Miscellaneous (NDMC)',
                        'Valid copy of Factory License (Mandatory) Common for all three corporation.',
                        'Valid copy of Health Trade License (Mandatory) Common for all three corporation.',
                        'Address proof in case of modification/change in address of applicant. (Conditional) Common for all three corporation.',
                        'Proof of ownership/ occupancy of the establishment or allotment letter of Govt. agency/tenancy proof (rent agreement)/Lease deed/Sale deed/GPA. (conditional) (SDMC) *in case change in ownership status (tenant/owner).',
                        'Old copy of license (NM) Common for all three corporation.',
                        'last paid renewal fee receipt (M) Common for all three corporation.',
                        'Proof of water supply/connection i.e. current water bill/ bore-well water testing report in case of modification/change in water supply. (NM)- Conditional (Common for all three corporation).',
                        'Proof which certifies that drainage system changed. (NM)- Conditional (Common for all three corporation)'],
                    'AMENDMENT': [
                        'Medical Fitness certificate issued by authorized registered medical practitioner (MBBS) certifying that the applicant and meat handler are free form any infectious and contagious disease. (M) (VTL031) (MPU) (NDMC)',
                        'Miscellaneous (NDMC)',
                        'Owner/Licensee Photo (Mandatory) Common for all three corporation.',
                        'Death Certificate of the license holder (Non mandatory) Conditional- Common for all three corporation',
                        'Certificate of the legal heirs of the deceased license holder (mandatory) Conditional- Common for all three corporation',
                        'NOC FROM REST OF THE LEGAL HEIRS IN THE FORM OF AFFIDAVIT TO TRANSFER THE LICENSE IN THE NAME OF THE ONE LEGAL HEIRS. (Mandatory) Conditional- Common for all three corporation.',
                        'Proof of change of constitution (conditional).- Common for all three corporation.',
                        'Proof of addition/deletion of partners in case of change in Partnership (conditional) Common for all three corporation.',
                    ],
                    'SURRENDER': ['Applicant ID Proof (SDMC/NDMC/EDMC',
                                  'Miscellaneous (NDMC)']
                },
                'HORSE BUGGY': {'NEW': ['Photograph of horse buggy with horse/mare. (M) - VTL026.',
                                        'DOB proof of owner like Birth Certificate,10th Certificate Aadhar Card/Passport/Driving License/Voter ID card. In case of non-availability of Age proof, the applicant may submit an undertaking in the form of affidavit regarding his/her age proof. (M) - VTL027.',
                                        'Document regarding Address proof. (M) - VTL028.',
                                        'Veterinary Heath certificate w.r.t Horse/mare issued by registered  Veterinary Doctor in (Delhi). (M)- VTL029',
                                        'Miscellaneous (NDMC)'],
                                'RENEWAL': [
                                    'Address proof (* in case of modification/change in address of applicant). Conditional based',
                                    'Photograph of horse buggy with horse/mare. (M)',
                                    'Vetrinary Heath certificate w.r.t Horse/mare issued by registered Veterinary Doctor in Delhi). (M)',
                                    'Miscellaneous (NDMC)',
                                    'Last paid Renewal License Fee Receipt (Mandatory)'],
                                'AMENDMENT': ['Owner/Licensee Photo (M)',
                                              'Death Certificate of the license holder (NM) Conditional',
                                              'Certificate of the legal heirs of the deceased license holder (NM) Conditional (VTL-013)',
                                              'NOC FROM REST OF THE LEGAL HEIRS IN THE FORM OF AFFIDAVIT TO TRANSFER THE LICENSE IN THE NAME OF THE ONE LEGAL HEIRS. (Conditional) (VTL-014)',
                                              'Proof of change of constitution (conditional).',
                                              'Proof of addition/deletion of partners in case of change in Partnership- Conditional',
                                              'Miscellaneous (NDMC)'],
                                'SURRENDER': ['Applicant ID Proof (SDMC/NDMC/EDMC)',
                                              'Miscellaneous (NDMC)']}
            },
            'FTL': {'NEW': {'CONFORMING INDUSTRIAL AREA': [
                ' Ownership/registered occupancy proof in shape of perpetual deed, lease deed alongwith NOC of owner (complete chain of ownership not required).',
                'Company details i.e., certificate of incorporation/MOU, authority letter in name of applicant/NOC of partner with partnership deed.',
                'Building plan or sanction letters i.e. Form C & D.',
                'Self-undertaking/Self declaration on letter head (No affidavit required)',
                'Additional/Optional documents, if any.',
                'DPCC consent.',
                'Fire NOC (If premises come under purview above 250 sqm).'],
                'DDA/DSIDC/DI BUILT-UP AUCTION/ALOTTED SHEDS': [
                    'Ownership/registered occupancy proof in shape of perpetual deed, lease deed alongwith NOC of owner (complete chain of ownership not required).',
                    'Company details i.e., certificate of incorporation/MOU, authority letter in name of applicant/NOC of partner with partnership deed.',
                    'Building plan or sanction letters i.e.  Form C & D.',
                    'Self-undertaking/Self declaration on letter head (No affidavit required)',
                    'Additional/Optional documents, if any.'
                    , 'DPCC consent.'
                    , 'Fire NOC (If premises come under purview above 250 sqm).'],
                'INDUSTRIES OUTSIDE INDUSTRIAL AREA': [
                    'Ownership/registered occupancy proof in shape of perpetual deed, lease deed alongwith NOC of owner (complete chain of ownership not required).',
                    'Company details i.e., certificate of incorporation/MOU, authority letter in name of applicant/NOC of partner with partnership deed.'
                    , 'Self-undertaking /Self declaration on letter head (No affidavit required)'
                    , 'Key plan/Site plan.'
                    , 'Additional/Optional documents, if any.'
                    , 'DPCC consent.'
                    , 'Fire NOC (If premises come under purview above 250 sqm).'],
                'HOUSEHOLD CATEGORY': [
                    'Ownership/registered occupancy proof /lease deed alongwith NOC of owner.',
                    'Details applicant i.e. Photo ID proof.'
                    , 'Copy of electricity bill & Site plan/key plan.'
                    , 'Self-undertaking /Self declaration on letter head (No affidavit required)'
                    , 'Additional/Optional documents, if any.'
                    , 'DPCC consent. (Not required being A category non-polluting trade)'],
                'LOCAL COMMERCIAL CATEGORY': [
                    'Ownership/registered occupancy proof /lease deed alongwith NOC of owner.'
                    , 'Copy of electricity bill.'
                    , 'Sanctioned building plan & site plan/key plan.'
                    , 'Self-undertaking /Self-declaration on letter head (No affidavit required)'
                    , 'DPCC consent'
                    , 'Certificate of safety of explosives.'
                    , 'Fire NOC (If premises come under purview above 250 sqm).']
            },
                'RENEWAL': ['DPCC ', 'Fire NOC (If area greater than 250 Sq. Mt)'],
                'AMENDMENT': [
                    'Constitution of firm/Incorporation certificate in case of public or private limited company. (for Change of constitution of firm)',
                    'NOC/Authority in favor of applicant (for change of name of director/partner).',
                    'Details of proposed machinery with H.P. rating. (For change in power load).',
                    'Undertaking on company letter head.',
                    'Consent from DPCC, If any, as per norms laid down for the applied industry (Required for all purposes and for change of trade)',
                    'Additional Undertaking/indemnity Bond/affidavit as prescribed for clusters of industrial concentration earmarked for redevelopment into conforming industrial areas as per MPD-2021'],
                'SURRENDER': ['UID', 'Undertaking']
            }
        }

        document_req_data = document_req_by_service

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

        if(10 != None):
            categories_str = ""
            idx = 1
            for category in 10:
                categories_str+= str(idx)+". "+category+"\n"
                idx+=1
            response_msg = "Following Trade Categories are available in {}:\n{}".format(service_name, categories_str)
        else:
            response_msg = "Couldn't find trade categories for {}. Please make sure you have typed the name correctly!".format(service_name)

        dispatcher.utter_message(text=response_msg)

        return []


class DocRequirementFinder():
    def find_doc_in_repo(self, service_name, licence_update_type, sub_category, doc_repo):
        service_name = service_name.upper()
        licence_update_type = licence_update_type.upper()
        sub_category = sub_category.upper()

        doc_list = None
        doc_repository = doc_repo

        if service_name == 'GTL':
            if service_name in doc_repository.keys():
                if licence_update_type in doc_repository[service_name].keys():
                    doc_list = doc_repository[service_name][licence_update_type]
                else:
                    response_msg = "Couldn't find {} in Licence Updating Types of {}. Please make sure you have " \
                                   "typed the name correctly".format(licence_update_type, service_name)
                    return response_msg
            else:
                response_msg = "Couldn't find {} in our Services. Please make sure you have typed the name correctly.".format(
                    service_name)
                return response_msg

        elif service_name == 'VTL':
            if service_name in doc_repository.keys():
                if sub_category != 'NONE':
                    for trade,_ in doc_repository[service_name].items():

                        regex_ptt = re.escape(sub_category) + "*"
                        isTradePresent = re.search(regex_ptt, trade)

                        if isTradePresent:
                            if licence_update_type in doc_repository[service_name][trade].keys():
                                doc_list = doc_repository[service_name][trade][licence_update_type]
                                if doc_list is not None:
                                    document_req_str = ""
                                    idx = 1
                                    for doc in doc_list:
                                        document_req_str += str(idx) + ". " + doc + "\n"
                                        idx += 1
                                    response_msg = "Following Documents are required for:- \n • Licence Type : {}\n • Service : {}\n • " \
                                                   "Trade Type : {}\n\n{}".format(licence_update_type, service_name,
                                                                                  trade,
                                                                                  document_req_str)
                                    return response_msg
                                else:
                                    response_msg = "Couldn't find Required Documents for {} in {}. Please make sure you have typed the name " \
                                                   "correctly.".format(licence_update_type, service_name)
                                    return response_msg
                            else:
                                response_msg = "Couldn't find {} in Licence Updating Types of {}. Please make sure you have typed the name correctly".format(
                                    licence_update_type, service_name)
                                return response_msg

                else:
                    response_msg = "Please specify the Trade Type for {}.".format(service_name)
                    return response_msg
            else:
                response_msg = "Couldn't find {} in our Services. Please make sure you have typed the " \
                               "name correctly.".format(service_name)
                return response_msg

        elif service_name == "FTL":
            if service_name in doc_repository.keys():
                if licence_update_type in doc_repository[service_name].keys():
                    if licence_update_type == "NEW":
                        if sub_category != "NONE":
                            for trade,_ in doc_repository[service_name][licence_update_type].items():

                                regex_ptt = re.escape(sub_category) + "*"
                                isTradePresent = re.search(regex_ptt, trade)

                                if isTradePresent:
                                    doc_list = doc_repository[service_name][licence_update_type][trade]
                                    if doc_list is not None:
                                        document_req_str = ""
                                        idx = 1
                                        for doc in doc_list:
                                            document_req_str += str(idx) + ". " + doc + "\n"
                                            idx += 1
                                        response_msg = "Following Documents are required for:- \n • Licence Type : {}\n • Service : {}\n • " \
                                                       "Trade Type : {}\n\n{}".format(licence_update_type, service_name,
                                                                                      trade,
                                                                                      document_req_str)
                                        return response_msg
                                    else:
                                        response_msg = "Couldn't find Required Documents for {} in {}. Please make sure you have typed the name " \
                                                       "correctly.".format(licence_update_type, service_name)
                                        return response_msg
                        else:
                            response_msg = "Please specify the Trade Type for {} in case of NEW Licence only.".format(
                                service_name)
                            return response_msg
                    else:
                        doc_list = doc_repository[service_name][licence_update_type]
                else:
                    response_msg = "Couldn't find {} in Licence Updating Types of {}. Please make sure you have " \
                                   "typed the name correctly".format(licence_update_type, service_name)
                    return response_msg
            else:
                response_msg = "Couldn't find {} in our Services. Please make sure you have typed the " \
                               "name correctly.".format(service_name)
                return response_msg

        if doc_list is not None:
            document_req_str = ""
            idx = 1
            for doc in doc_list:
                document_req_str += str(idx) + ". " + doc + "\n"
                idx += 1
            response_msg = "Following Documents are required for:- \n • Licence Type : {}\n • Service : {}\n • " \
                           "Trade Type : {}\n\n{}".format(licence_update_type, service_name, sub_category,
                                                          document_req_str)
            return response_msg
        else:
            response_msg = "Couldn't find Required Documents for {} in {}. Please make sure you have typed the name " \
                           "correctly.".format(licence_update_type, service_name)
            return response_msg


