import streamlit as st
from config import server_url

def show_home():
    st.title("API Testing Overview")

    st.write("""
    ## What is an API?
    - An **Application Programming Interface (API)** allows software applications to communicate with each other. It exposes a set of definitions and protocols for building and integrating application software.
    - APIs can be used for both web communication (web services) and local data exchange (offline APIs).
    
    ## API and Web Services
    - **Web services** use APIs for communication over the web using HTTP/HTTPS protocols, supporting formats like XML and JSON.
    - While all web services are APIs, not all APIs are web services.

    ## HTTP Methods
    - HTTP defines several **request methods** to indicate the desired action to be performed for a given resource. Notable methods include GET, POST, PUT, DELETE, which are used for retrieving, submitting, updating, and deleting data, respectively.

    ## Safe and Idempotent Methods
    - **Safe methods** like GET, HEAD, OPTIONS, and TRACE don't alter the server state and are used for read-only operations.
    - **Idempotent methods** ensure that multiple identical requests have the same effect as a single request. PUT and DELETE are idempotent but not safe.

    ## Status Codes
    - HTTP responses are accompanied by **status codes** indicating the outcome of the request. They range from informational (1xx), success (2xx), redirection (3xx), client errors (4xx), to server errors (5xx).

    ## API Testing
    - **API Testing** involves testing APIs directly and as part of integration testing to determine if they meet expectations for functionality, reliability, performance, and security.
    
    ## Test Coverage
    - A comprehensive API test strategy should include tests for validating all input and output parameters, authentication, authorization, error codes, and ensuring proper handling of valid and invalid data.
    """)

    st.write("For more details on API testing and best practices, visit the API documentation and resources available online.")
