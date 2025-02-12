#!/bin/bash

# Function to print section header
print_section() {
    echo -e "\n\n==== $1 ====\n"
}

# Function to handle curl with error details
curl_with_error_details() {
    local url="$1"
    local method="${2:-GET}"
    local data="${3:-}"
    
    echo "URL: $url"
    echo "Method: $method"
    
    if [ "$method" == "GET" ]; then
        response=$(curl -s -v -w "\nHTTP Status: %{http_code}" "$url" 2>&1)
    else
        response=$(curl -s -v -X "$method" "$url" -H "Content-Type: application/json" -d "$data" -w "\nHTTP Status: %{http_code}" 2>&1)
    fi
    
    echo "$response"
    echo "---"
}

# Dashboard Endpoints
print_section "Dashboard Endpoints"
curl_with_error_details "http://localhost:5000/api/dashboard/last_study_session/"
curl_with_error_details "http://localhost:5000/api/dashboard/study_progress/"
curl_with_error_details "http://localhost:5000/api/dashboard/quick-stats/"

# Words Endpoints
print_section "Words Endpoints"
curl_with_error_details "http://localhost:5000/api/words/"
curl_with_error_details "http://localhost:5000/api/words/1/"
curl_with_error_details "http://localhost:5000/api/words/" "POST" '{"japanese":"\u3053\u3093\u306b\u3061\u306f","romaji":"konnichiwa","english":"hello"}'

# Groups Endpoints
print_section "Groups Endpoints"
curl_with_error_details "http://localhost:5000/api/groups/"
curl_with_error_details "http://localhost:5000/api/groups/1/"
curl_with_error_details "http://localhost:5000/api/groups/1/words/"
curl_with_error_details "http://localhost:5000/api/groups/" "POST" '{"name":"Basic Greetings"}'

# Study Activities Endpoints
print_section "Study Activities Endpoints"
curl_with_error_details "http://localhost:5000/api/study-activities/"
curl_with_error_details "http://localhost:5000/api/study-activities/1/"
curl_with_error_details "http://localhost:5000/api/study-activities/" "POST" '{"name":"Vocabulary Quiz","description":"Test your vocabulary skills","thumbnail_url":"/thumbnails/vocab_quiz.jpg"}'

# Study Sessions Endpoints
print_section "Study Sessions Endpoints"
curl_with_error_details "http://localhost:5000/api/study-sessions/"
curl_with_error_details "http://localhost:5000/api/study-sessions/1/"
curl_with_error_details "http://localhost:5000/api/study-sessions/" "POST" '{"study_activity_id":1,"group_id":1}'
curl_with_error_details "http://localhost:5000/api/study-sessions/1/word-reviews/" "POST" '{"word_id":1,"correct":true}'
