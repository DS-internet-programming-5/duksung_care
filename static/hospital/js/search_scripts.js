// Enter 키 입력을 감지하는 함수
document.getElementById("searchQuery").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault(); // 기본 동작 방지 (폼 제출 등)
        searchHospitals();
    }
});
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