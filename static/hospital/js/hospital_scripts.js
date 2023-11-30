// 리뷰 목록 클릭시 새로고침 없이 오프캔버스 열리게 함
$(document).ready(function () {
    // 평균 별점 표시
    displayRatings();

    // 병원 목록 클릭시 상세보기
    $('.hospital-detail-link').on('click', function (e) {
        e.preventDefault();

        var hospitalPk = $(this).data('hospital-pk');
        console.log(hospitalPk);

        $.ajax({
            type: 'GET',
            url: `/hospital/${hospitalPk}/`, // URL to fetch hospital detail
            success: function (data) {
                $('.offcanvas').html(data);
                var hospitalDetail = $('<div>').html(data); // Create a temporary element to parse the HTML content
                var hospitalY = hospitalDetail.find('.div-detail').data('latitude');
                var hospitalX = hospitalDetail.find('.div-detail').data('longitude');
                console.log(hospitalY, hospitalX);

                // panTo 함수 호출하여 해당 위치로 지도 이동
                panTo(hospitalY, hospitalX);
                displayRatings();
            },
            error: function (xhr, status, error) {
                console.error(error); // Handle errors if any
            }
        });
    });

    // 북마크
    const csrfToken = document.getElementById('csrf-token').value;
    $('.bookmark-btn').click(function() {
        const hospitalId = $(this).data('hospital-pk');
        console.log(hospitalId);

        $.ajax({
            type: 'POST',
            url: `/hospital/${hospitalId}/bookmark/`,
            data: {
                csrfmiddlewaretoken: csrfToken,
            },
            success: function(response) {
                if (response.bookmarked) {
                    $(`.bookmark-btn[data-hospital-pk="${hospitalId}"] i`).css('color', '#0174BE');
                } else {
                    $(`.bookmark-btn[data-hospital-pk="${hospitalId}"] i`).css('color', 'darkgray');
                }
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    });
});

// 평균 별점 표시
function displayRatings (){
    var ratings = $('.avg-rating .rating-avg');

    ratings.each(function () {
        var $this = $(this);
        var targetScore = $(this).attr('data-rate');
        var firstDigit = targetScore.split('.');

        if(firstDigit.length > 1){
            for(var i=0;i<firstDigit[0];i++){
                $this.find('.star-avg').eq(i).css({width:'100%'})
            }
            $this.find('.star-avg').eq(firstDigit[0]).css({width:firstDigit[1]+'0%'})
        }
        else{
            for(var i=0;i<targetScore;i++){
                $this.find('.star-avg').eq(i).css({width:'100%'})
            }
        }
    });
}

// 별점 업데이트 함수
function updateRatings(hospital_pk, targetScore, num_reviews) {
    var ratings = $('#avg-rating-' + hospital_pk + ' .rating-avg');
    var rating_text = $('.rating-text-' + hospital_pk);
    var review_count = $('.num-reviews-' + hospital_pk);
    targetScore = parseFloat(targetScore).toFixed(1);

    console.log('updateRatings: ' + targetScore);
    console.log(ratings);
    console.log(rating_text);

    ratings.each(function () {
        var $this = $(this);
        $this.attr('data-rate', targetScore);
        var firstDigit = targetScore.toString().split('.');
        console.log(firstDigit);

        for(var i=0;i<5;i++){
            $this.find('.star-avg').eq(i).css({width:'0%'})
        }
        for(var i=0;i<firstDigit[0];i++){
            $this.find('.star-avg').eq(i).css({width:'100%'})
        }
        $this.find('.star-avg').eq(firstDigit[0]).css({width:firstDigit[1]+'0%'})
    });

    var formattedScore = parseFloat(targetScore).toFixed(1);
    rating_text.text(formattedScore);
    review_count.text(num_reviews);
}

// 카테고리 선택 또는 정렬 기준 변경 시 병원 목록 페이지로 이동
function redirectToHospitalList() {
    var categoryOption = document.getElementById('categorySelect').value;
    var orderOption = document.querySelectorAll('.form-select')[1].value;

    var baseUrl = '/hospital/';
    var queryParams = [];

    if (categoryOption !== '') {
        baseUrl += 'category/' + categoryOption + '/';
    }

    const urlParams = new URLSearchParams(window.location.search);
    const pageParam = urlParams.get('page');
    if (pageParam) {
        queryParams.push('page=' + pageParam);
    } else {
        queryParams.push('page=1');
    }

    if (orderOption !== '정렬기준') {
        queryParams.push('order=' + orderOption);
    }

    var filterOptions = [];
    document.querySelectorAll('.form-check-input').forEach(checkbox => {
        if (checkbox.checked) {
            filterOptions.push(checkbox.id);
        }
    });

    if (filterOptions.length > 0) {
        queryParams.push('filter=' + filterOptions.join(','));
    }

    var bookmarkButton = document.getElementById('bookmarkButton');
    if (bookmarkButton.classList.contains('active')) {
        queryParams.push('bookmark=true');
    }
    else {
        // 북마크 버튼이 비활성화되었을 때 해당 필터를 제거
        var index = queryParams.indexOf('bookmark=true');
        if (index > -1) {
            queryParams.splice(index, 1);
        }
    }

    if (queryParams.length > 0) {
        baseUrl += '?' + queryParams.join('&');
    }

    window.location.href = baseUrl;
}

// 카테고리 선택 또는 정렬 기준 변경 이벤트
document.querySelectorAll('.form-select').forEach(select => {
    select.addEventListener('change', redirectToHospitalList);
});

// 상세 설정 체크박스 변경 이벤트
document.querySelectorAll('.form-check-input').forEach(input => {
    input.addEventListener('change', redirectToHospitalList);
});

// 북마크 버튼 클릭 시 이벤트
document.getElementById('bookmarkButton').addEventListener('click', function() {
    redirectToHospitalList();
});

// 현재 URL에서 order 매개변수 가져오기
const urlParams = new URLSearchParams(window.location.search);
const orderParam = urlParams.get('order');
const filterParam = urlParams.get('filter');
const bookmarkParam = urlParams.get('bookmark');

// 정렬 기준 select 엘리먼트 가져오기
const orderSelect = document.querySelector('.order-select');
const filterCheckboxes = document.querySelectorAll('.form-check-input');
const bookmarkButton = document.getElementById('bookmarkButton');

// order 매개변수 값에 따라 정렬 기준을 설정
if (orderParam) {
    const options = orderSelect.options;
    for (const option of options) {
        if (option.value === orderParam) {
            option.setAttribute('selected', 'selected');
            break;
        }
    }
}

// filter 매개변수 값에 따라 체크박스 상태 설정
if (filterParam) {
    console.log(filterParam);
    const filters = filterParam.split(',');
    filterCheckboxes.forEach(checkbox => {
        if (filters.includes(checkbox.id)) {
            checkbox.checked = true;
            checkbox.value = true;
        }
    });
}

if (bookmarkParam && bookmarkParam === 'true') {
    bookmarkButton.classList.add('active');
}

function changePage(page) {
        const urlParams = new URLSearchParams(window.location.search);
        urlParams.set('page', page);
        window.location.href = '?' + urlParams.toString();
    }
