#function responsible to the sent_data that will is going to be request.args or request.json and the
# expected_data taht is going to be the list of keys the endpoint requires
# this function will return a string in case of error and None otherwise
def check_endpoint_info(sent_data, expected_data):
    for data in expected_data:
        if(sent_data.get(data) == None):
            return f"The {data} argument is required."