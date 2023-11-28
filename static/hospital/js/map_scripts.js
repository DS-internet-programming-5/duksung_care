var mapContainer = document.getElementById('map'), // 지도를 표시할 div
    mapOption = {
        center: new kakao.maps.LatLng(37.64998176552163, 127.01680486039935), // 지도의 중심좌표
        level: 4 // 지도의 확대 레벨
    };

// 지도를 생성합니다
var map = new kakao.maps.Map(mapContainer, mapOption);

// 지도 센터로 부드럽게 이동
function panTo(y, x) {
    // 이동할 위도 경도 위치를 생성합니다
    var moveLatLon = new kakao.maps.LatLng(y, x);

    console.log("panTo 호출")
    map.setLevel(3)
    map.panTo(moveLatLon);
}

// 지도 센터로 이동
function setCenter(y, x) {
    // 이동할 위도 경도 위치를 생성합니다
    var moveLatLon = new kakao.maps.LatLng(y, x);

    // 지도 중심을 이동 시킵니다
    map.setCenter(moveLatLon);

}

// DB에 저장된 병원 목록으로 마커 표시
fetch('/hospital/get_hospital_list') // 서버에서 hospital_list를 반환하는 엔드포인트
    .then(response => response.json())
    .then(data => {
            var order = document.getElementById('HP8').getAttribute('data-order');
            for (let i = 0; i < data.length; i++) {
                const hospital = data[i];
                const markerPosition = new kakao.maps.LatLng(hospital.y, hospital.x);

                const imageSrc = 'https://cdn4.iconfinder.com/data/icons/essentials-72/24/025_-_Location-512.png'; // 마커 이미지 url
                // const imageSrc = 'https://cdn.iconfinder.com/stored_data/1388462/128/png?token=1700871706-RMv8idjAKgte%2FejVd11%2BPvwjMh0kUK2A%2FE0w3rss2WQ%3D'; // 마커 이미지 url
                const imageSize = new kakao.maps.Size(30, 30);  // 마커 이미지의 크기
                const imgOptions = {
                    // spriteSize: new kakao.maps.Size(72, 208), // 스프라이트 이미지의 크기
                    // spriteOrigin: new kakao.maps.Point(46, (order * 36)), // 스프라이트 이미지 중 사용할 영역의 좌상단 좌표
                    offset: new kakao.maps.Point(15, 30) // 마커 좌표에 일치시킬 이미지 내에서의 좌표
                };
                const markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions);

                // 마커 생성
                const marker = new kakao.maps.Marker({
                    position: markerPosition,
                    image: markerImage
                });

                // 지도에 마커 추가
                marker.setMap(map);

                // 마커 클릭 이벤트 리스너 등록
                kakao.maps.event.addListener(marker, 'click', function (e) {

                    // Offcanvas 요소가 열려있는지 확인
                    var offcanvasElement = document.getElementById('offcanvasScrolling');
                    var isOffcanvasOpen = offcanvasElement.getAttribute('aria-modal') === 'true';

                    $.ajax({
                        type: 'GET',
                        url: `/hospital/${hospital.pk}/`,
                        success: function (data) {
                            if (isOffcanvasOpen) {
                                // Offcanvas가 열려있으면 offcanvas 내용 업데이트
                                $('.offcanvas').html(data);
                            } else {
                                // Offcanvas가 닫혀있으면 offcanvas 열고 내용 업데이트
                                $('.offcanvas').html(data);
                                var myOffcanvas = new bootstrap.Offcanvas(offcanvasElement);
                                myOffcanvas.show();
                            }
                            console.log(data);
                        },
                        error: function (xhr, status, error) {
                            console.error(error); // 에러 처리
                        }
                    });

                    // 지도 중심좌표 이동
                    panTo(hospital.y, hospital.x);
                    e.preventDefault(); // a 태그의 기본 동작 취소 (링크 이동 막기)

                });
            }
        }
        // fetch 실패
    ).catch(error => {
    console.log(error);
});