// Enter 키 입력을 감지하는 함수
const searchQueryElement = document.getElementById("searchQuery");

if (searchQueryElement) {
    searchQueryElement.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            event.preventDefault(); // 기본 동작 방지 (폼 제출 등)
            searchHospitals();
        }
    });
}
// 병원 검색
function searchHospitals() {
    const searchQuery = document.getElementById('searchQuery').value.trim();
    const baseUrl = '/hospital/';

    let queryString = '';
    const urlParams = new URLSearchParams(window.location.search);
    const pageParam = urlParams.get('page');

    if (searchQuery !== '') {
        queryString += `?search_query=${encodeURIComponent(searchQuery)}`;
    }

    console.log(pageParam);

    if (pageParam === null) {
        queryString += `${queryString ? '&' : '?'}page=1`;
    }
    else if (pageParam) {
        queryString += `${queryString ? '&' : '?'}page=${pageParam}`;
    }

    window.location.href = baseUrl + queryString;
}

// 종류별로 찾기
const buttons = document.getElementsByClassName('btn-primary-type');
console.log(buttons);
Array.from(buttons).forEach(button => {
    button.addEventListener('click', function(event) {
        event.preventDefault(); // 클릭 이벤트의 기본 동작을 막음
        const category = this.textContent.trim(); // 클릭된 버튼의 텍스트 콘텐츠를 가져옴
        searchByCategory(category); // searchByCategory 함수 호출
    });
});

function searchByCategory(category) {
    const baseUrl = '/hospital/category/';
    const urlParams = new URLSearchParams(window.location.search);
    const pageParam = urlParams.get('page');
    let queryString = '';

    if (pageParam === null) {
        queryString += `${queryString ? '&' : '?'}page=1`;
    } else if (pageParam) {
        queryString += `${queryString ? '&' : '?'}page=${pageParam}`;
    }

    window.location.href = baseUrl + category + queryString;
}