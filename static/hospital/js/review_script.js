$(document).ready(function () {
    // 리뷰 작성 버튼 클릭시
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
                console.log(createdAt.toLocaleString('ko-KR', {timeZone: 'Asia/Seoul'}));
                var formattedDate = createdAt.toLocaleString('ko-KR', {
                    timeZone: 'Asia/Seoul',
                    year: 'numeric',
                    month: '2-digit',
                    day: '2-digit'
                })
                    .replace(/\.\s/g, '.');

                console.log(data);
                // 리뷰가 성공적으로 추가되면 해당 리뷰를 화면에 동적으로 추가
                // $('.review-list').append(`<div class="review"><div class="rating" data-rate="${data.hospital_rating}">${getStars(data.hospital_rating)}</div></div>`);
                // $('.review-list').append(`<p>${data.content}</p>`);
                var reviewCard = `
                    <div class="card review-card-${data.review_pk} mt-3 p-3" data-review-id="${data.review_pk}">
                        <div class="d-flex align-items-center justify-content-between">
                            <div class="d-flex align-items-center">
                                <div class="review-profile-box d-flex justify-content-center align-content-center"
                                     style="width: 40px; height: 40px; background-color: #FFF0CE; border-radius: 70%">
                                    ${data.profileImg ? `<img src="${data.profileImg}"
                                         style="width: 100%; height: 100%; object-fit: cover; border-radius: 70%;">` :
                                        `<img src="${defaultProfileImg}"
                                             style="width:80%; height:80%; margin: auto; object-fit: cover">`}
                                </div>
                                <span style="margin-left: 10px">${data.nickname}</span>
                                    <span class="time" style="margin-left: 10px; color: gray"> | ${formattedDate}</span>
                            </div>
                            <!-- 수정, 삭제 버튼 -->
                            <div>
                                <a class="update-link" data-bs-toggle="modal" href="#updateModal" data-review-id="${data.review_pk}"
                                data-review-content="${data.content}" data-hospital-rating="${data.hospital_rating}">수정</a>
                                <a class="delete-link" data-bs-toggle="modal" href="#deleteModal" data-review-id="${data.review_pk}">삭제</a>
                            </div>
                        </div>
                        <div class="review mt-2">
                            <div class="rating" data-rate="${data.hospital_rating}">
                                ${getStars(data.hospital_rating)}
                            </div>
                            <p class="r-content mt-2 mb-0" style="white-space:pre;">${data.content}</p>
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

// 리뷰 수정
$(document).ready(function () {
    var review_id;
    // 입력칸에 원래 리뷰 내용 초기에 불러와서 표시
    $('#updateModal').on('show.bs.modal', function (event) {
        var triggerElement = $(event.relatedTarget); // 모달을 여는 요소 (수정 링크)

        // data-review-content 속성 값 가져오기
        var reviewContent = triggerElement.data('review-content');
        // data-hospital-rating 속성 값 가져오기
        var hospitalRating = triggerElement.data('hospital-rating');

        review_id = triggerElement.data('review-id');

        console.log('load hospitalRating: ' + hospitalRating);
        console.log('load review_id: ' + review_id);

        // textarea에 review-content 값 설정
        $('#review-update-form textarea[name="content"]').val(reviewContent);

        // select에 hospital-rating 값 설정
        $('#review-update-form select[name="hospital_rating"]').val(hospitalRating);

        // 별점 로드
        $('.make_star_update i').css({color: 'lightgrey'});
        $('.make_star_update i:nth-child(-n+' + hospitalRating + ')').css({color: '#FFC436'});
    });
    $('#review-update-form').submit(function (e) {
        e.preventDefault();

        var formData = $(this).serialize();

        console.log('update: ' + review_id);

        var url = `/hospital/update_review/${review_id}/`;

        console.log(formData);

        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            success: function (data) {
                const defaultProfileImg = '../../static/imgs/default_profile.png';
                var createdAt = new Date();
                console.log(createdAt.toLocaleString('ko-KR', {timeZone: 'Asia/Seoul'}));
                var formattedDate = createdAt.toLocaleString('ko-KR', {
                    timeZone: 'Asia/Seoul',
                    year: 'numeric',
                    month: '2-digit',
                    day: '2-digit'
                })
                    .replace(/\.\s/g, '.');

                console.log("update: " + data);
                console.log("update: ", JSON.stringify(data));

                // 리뷰가 성공적으로 수정되면 해당 내용을 모달에 표시
                const modalBody = $('#updateModal .modal-body');
                // 기존 내용 감추기
                modalBody.find('.original-content').hide();
                // 수정 성공 문구 보이기
                modalBody.find('.success-message').show();

                // 기존의 내용 초기화
                $('#review-update-form textarea[name="content"]').val('');
                $('.make_star i').css({color: 'lightgrey'});

                const updatedContent = data.content; // 수정된 내용
                const updatedRating = data.hospital_rating; // 수정된 평점

                // 리뷰 카드 업데이트 함수 호출
                updateReviewCard(review_id, updatedContent, updatedRating, formattedDate);
            },
            error: function (xhr, status, error) {
                console.error(error);
            }
        });
        // 모달을 닫았을 때
        $('#updateModal').on('hidden.bs.modal', function (e) {
            const modalBody = $(this).find('.modal-body');
            // 기존 내용 보이기
            modalBody.find('.original-content').show();
            // 수정 성공 문구 감추기
            modalBody.find('.success-message').hide();
        });
    });

});

// 리뷰 카드 업데이트 함수
function updateReviewCard(reviewId, updatedContent, updatedRating, updatedDate) {
    const reviewCard = $(`.review-card-${reviewId}`);
    console.log(reviewCard);
    console.log(reviewId);

    // 리뷰 내용 업데이트
    reviewCard.find('.r-content').text(updatedContent);
    reviewCard.find('.time').text(updatedDate);

    // 별점 업데이트
    const ratingStars = reviewCard.find('.rating');
    ratingStars.empty();
    ratingStars.append(`<div class="rating" data-rate="${updatedRating}">
                                ${getStars(updatedRating)}
                            </div>`);

    // 수정 버튼의 review-content와 hospital-rating 값 업데이트
    const updateLink = reviewCard.find(`.update-link[data-review-id="${reviewId}"]`);
    console.log(updateLink);
    updateLink.data('review-content', updatedContent);
    updateLink.data('hospital-rating', updatedRating);
}

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

// 리뷰 작성 별점 표시
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

// 리뷰 수정 별점 표시
$(function () {
    var userScore_update = $('#makeStar_update');
    userScore_update.change(function () {
        var userScoreNum = $(this).val();
        console.log(userScoreNum);
        $('.make_star_update i').css({color: 'lightgrey'});
        $('.make_star_update i:nth-child(-n+' + userScoreNum + ')').css({color: '#FFC436'});
    });

    $('.make_star_update i').click(function () {
        var targetNum = $(this).index() + 1;
        $('.make_star_update i').css({color: 'lightgrey'});
        var hospitalRatingSelect = $('#makeStar_update');
        hospitalRatingSelect.val(targetNum);
        $('.make_star_update i:nth-child(-n+' + targetNum + ')').css({color: '#FFC436'});
    })
})

// 리뷰 삭제
$(document).ready(function () {
    $('#review-delete-form').submit(function (e) {
        e.preventDefault();

        var review_id = $('.delete-link').data('review-id');
        var formData = $(this).serialize();

        var url = `/hospital/delete_review/${review_id}/`;

        console.log(formData);

        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            success: function (data) {
                console.log("update: " + data);
                console.log("update: ", JSON.stringify(data));

                // 리뷰가 성공적으로 삭제되면 해당 내용을 모달에 표시
                const modalBody = $('#deleteModal .modal-body');
                // 기존 내용 감추기
                modalBody.find('.original-content').hide();
                // 삭제 성공 문구 보이기
                modalBody.find('.success-message').show();

                // 리뷰 카드 업데이트 함수 호출
                deleteReviewCard(review_id);
            },
            error: function (xhr, status, error) {
                console.error(error);
            }
        });
        // 모달을 닫았을 때
        $('#deleteModal').on('hidden.bs.modal', function (e) {
            const modalBody = $(this).find('.modal-body');
            // 기존 내용 보이기
            modalBody.find('.original-content').show();
            // 수정 성공 문구 감추기
            modalBody.find('.success-message').hide();
        });
    });
});

// 리뷰 카드 삭제 함수
function deleteReviewCard(reviewId) {
    const reviewCard = $(`.review-card-${reviewId}`);
    console.log(reviewCard);

    // 리뷰 카드를 서서히 사라지도록 애니메이션 효과 적용
    reviewCard.fadeOut('slow', function () {
        // 카드가 사라진 후에 카드 요소를 완전히 제거
        $(this).remove();
    });

}