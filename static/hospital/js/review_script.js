$(document).ready(function () {
    $('#review-form').submit(function (e) {
        e.preventDefault();

        var formData = $(this).serialize();
        var hospitalPk = $(this).data('hospital-pk');
        var url = `/hospital/new_review/${hospitalPk}/`;

        console.log(formData);

        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            success: function (data) {
                const defaultProfileImg = '../../static/imgs/default_profile.png';
                var createdAt = new Date();
                console.log(createdAt.toLocaleString('ko-KR', { timeZone: 'Asia/Seoul' }));
                var formattedDate = createdAt.toLocaleString('ko-KR', { timeZone: 'Asia/Seoul', year: 'numeric', month: '2-digit', day: '2-digit' })
                    .replace(/\.\s/g, '.');

                console.log(data);
                // 리뷰가 성공적으로 추가되면 해당 리뷰를 화면에 동적으로 추가
                // $('.review-list').append(`<div class="review"><div class="rating" data-rate="${data.hospital_rating}">${getStars(data.hospital_rating)}</div></div>`);
                // $('.review-list').append(`<p>${data.content}</p>`);
                var reviewCard = `
                    <div class="card review-card review-list mt-3 p-3">
                        <div class="d-flex align-items-center justify-content-between">
                            <div class="d-flex align-items-center">
                                <div class="review-profile-box d-flex justify-content-center align-content-center"
                                     style="width: 40px; height: 40px; background-color: #FFF0CE; border-radius: 70%">
                                    ${data.profileImg ? `<img src="${data.profileImg}"
                                         style="width: 100%; height: 100%; object-fit: cover">` :
                                        `<img src="${defaultProfileImg}"
                                             style="width:80%; height:80%; margin: auto; object-fit: cover">`}
                                </div>
                                <span style="margin-left: 10px">${data.nickname}</span>
                                <span style="margin-left: 10px; color: gray"> | ${formattedDate}</span>
                            </div>
                            <!-- 수정, 삭제 버튼 -->
                            <div>
                                <a>수정</a>
                                <a>삭제</a>
                            </div>
                        </div>
                        <div class="review mt-2">
                            <div class="rating" data-rate="${data.hospital_rating}">
                                ${getStars(data.hospital_rating)}
                            </div>
                            <p class="mt-2 mb-0">${data.content}</p>
                        </div>
                    </div>
                `;
                $('.review-list-box').prepend(reviewCard);
                $('#review-form textarea[name="content"]').val('');
                $('.make_star i').css({color: 'lightgrey'});
            },
            error: function (xhr, status, error) {
                console.error(error);
            }
        });
    });
});

function getStars(rating) {
    var starsHTML = '';
    for (var i = 0; i < 5; i++) {
        if (i < rating) {
            starsHTML += '<i class="fas fa-star" style="color: #FFC436"></i> ';
        } else {
            starsHTML += '<i class="fas fa-star" style="color: lightgrey"></i> ';
        }
    }
    return starsHTML;
}

$(function () {
    var rating = $('.review .rating');

    rating.each(function () {
        var targetScore = $(this).attr('data-rate');
        console.log(targetScore);
        $(this).find('i:nth-child(-n+' + targetScore + ')').css({color: '#FFC436'})
    });

    var userScore = $('#makeStar');
    userScore.change(function () {
        var userScoreNum = $(this).val();
        console.log(userScoreNum);
        $('.make_star i').css({color: 'lightgrey'});
        $('.make_star i:nth-child(-n+' + userScoreNum + ')').css({color: '#FFC436'});
    });

    $('.make_star i').click(function () {
        var targetNum = $(this).index() + 1;
        $('.make_star i').css({color: 'lightgrey'});
        var hospitalRatingSelect = $('#makeStar');
        hospitalRatingSelect.val(targetNum);
        $('.make_star i:nth-child(-n+' + targetNum + ')').css({color: '#FFC436'});
    })
})