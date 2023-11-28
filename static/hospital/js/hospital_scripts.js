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
            },
            error: function (xhr, status, error) {
                console.error(error); // Handle errors if any
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

        console.log('targetScore: ', targetScore);
    });
}

// 카테고리 선택시 해당 카테고리 페이지로 이동
document.getElementById('categorySelect').addEventListener('change', function() {
    var selectedOption = this.value;
    if (selectedOption) {
        window.location.href = selectedOption;
    }
});
