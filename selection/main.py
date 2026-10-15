from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
# CORS 설정: 모든 도메인(GAS 웹 앱 포함)에서의 접근을 허용합니다.
CORS(app, resources={r"/sort": {"origins": "*"}})

def selection_sort_steps(arr):
    """
    단순 선택 정렬(Selection Sort)을 수행하면서 각 단계별 상태를 기록하여 반환합니다.
    - arr: 정렬할 숫자 리스트
    - returns: 각 단계별 배열 상태, 비교 중인 인덱스, 최소값 인덱스 등이 담긴 리스트
    """
    steps = []
    n = len(arr)
    
    # 초기 상태 기록
    steps.append({
        "array": list(arr),
        "message": "초기 배열 상태입니다.",
        "comparing": [],
        "min_index": -1,
        "sorted_indices": []
    })
    
    sorted_indices = []
    
    for i in range(n - 1):
        min_idx = i
        steps.append({
            "array": list(arr),
            "message": f"패스 {i+1}: 인덱스 {i}부터 시작. 현재 최소값 후보로 인덱스 {min_idx} (값: {arr[min_idx]}) 설정",
            "comparing": [i],
            "min_index": min_idx,
            "sorted_indices": list(sorted_indices)
        })
        
        for j in range(i + 1, n):
            steps.append({
                "array": list(arr),
                "message": f"인덱스 {j} (값: {arr[j]})와 현재 최소값(인덱스 {min_idx}, 값: {arr[min_idx]}) 비교 중",
                "comparing": [min_idx, j],
                "min_index": min_idx,
                "sorted_indices": list(sorted_indices)
            })
            
            if arr[j] < arr[min_idx]:
                min_idx = j
                steps.append({
                    "array": list(arr),
                    "message": f"더 작은 값 발견! 새로운 최소값 인덱스 {min_idx} (값: {arr[min_idx]})로 갱신",
                    "comparing": [min_idx],
                    "min_index": min_idx,
                    "sorted_indices": list(sorted_indices)
                })
        
        # 찾은 최소값과 현재 위치(i)의 값을 교환 (스왑)
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            steps.append({
                "array": list(arr),
                "message": f"최소값 인덱스 {min_idx}와 위치 {i}의 값을 교환(Swap)",
                "comparing": [i, min_idx],
                "min_index": min_idx,
                "sorted_indices": list(sorted_indices)
            })
        else:
            steps.append({
                "array": list(arr),
                "message": f"인덱스 {i}의 값이 이미 제자리에 있어 교환 없음",
                "comparing": [i],
                "min_index": min_idx,
                "sorted_indices": list(sorted_indices)
            })
            
        sorted_indices.append(i)
        
    # 마지막 원소까지 정렬 완료 처리
    sorted_indices.append(n - 1)
    steps.append({
        "array": list(arr),
        "message": "단순 선택 정렬이 성공적으로 완료되었습니다!",
        "comparing": [],
        "min_index": -1,
        "sorted_indices": list(sorted_indices)
    })
    return steps

@app.route('/sort', methods=['POST', 'OPTIONS'])
def sort_endpoint():
    """
    클라이언트로부터 숫자들이 담긴 배열을 받아 단순 선택 정렬 단계별 결과를 반환하는 API 엔드포인트
    """
    if request.method == 'OPTIONS':
        return '', 204

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON 데이터가 전달되지 않았습니다."}), 400
            
        arr = data.get('array', [64, 25, 12, 22, 11])
        
        # 입력값 검증 (숫자 리스트인지 확인)
        if not isinstance(arr, list) or not all(isinstance(x, (int, float)) for x in arr):
            return jsonify({"error": "유효한 숫자 배열을 전달해주세요."}), 400
            
        steps = selection_sort_steps(arr)
        
        return jsonify({
            "status": "success",
            "steps": steps,
            "complexity": {
                "time_worst": "O(n^2)",
                "time_best": "O(n^2)",
                "space": "O(1)"
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/', methods=['GET'])
def health_check():
    """서버 정상 작동 여부를 확인하는 헬스체크 엔드포인트"""
    return jsonify({"status": "online", "message": "Selection Sort Cloud Run Server is running!"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
