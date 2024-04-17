import requests
import time

def post_data_to_api(data, api_endpoint):
    try:
        response = requests.post(api_endpoint, json=data)
        if response.status_code == 201:
            print("Data posted successfully!")
        else:
            print("Failed to post data. Status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", str(e))

def update_data_to_api(data, api_endpoint):
    try:
        response = requests.put(api_endpoint, json=data)
        if response.status_code == 201:
            print("Data updated successfully!")
        else:
            print("Failed to update data. Status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", str(e))

def delete_data_from_api(api_endpoint):
    try:
        response = requests.delete(api_endpoint)
        if response.status_code == 201:
            print("Data deleted successfully!")
        else:
            print("Failed to delete data. Status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", str(e))


def main():
    api_endpoint = "http://localhost:5000/customers" 

    num_iterations = 10  
    ### Code for customer creation
    # for i in range(num_iterations):
    #     print("Iteration:", i+1)
    #     data = {"name": "value"+str(i),"email":"val"+str(i)+"@gamil.com"} 
    #     post_data_to_api(data, api_endpoint)

    ### Code for customer updation 
    # update_arr=['558432','568952','860435','002358','243895' ,'674630','853073','120786','623337','116129'] # array containing ids of fields need to be updated
    # for i in range(num_iterations):
    #     print("Update interaction:", i+1)
    #     data = {"name": "value"+str(i) + str(i),"email":"val"+str(i)+ str(i)+"@gamil.com"} 
    #     update_data_to_api(data,api_endpoint+'/'+update_arr[i])
    
    ### Code for customer deletion
    # delete_arr=['558432','568952','860435','002358','243895' ,'674630','853073','120786','623337','116129'] # array containing ids of fields need to be deleted
    # for i in range(num_iterations):
    #     print("Delete interaction:", i+1)
    #     delete_data_from_api(api_endpoint+'/'+delete_arr[i])

    

if __name__ == "__main__":
    main()
