import re


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
