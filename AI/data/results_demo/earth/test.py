import obspy

# MiniSEED 파일 경로
file_path = './earth_original_seismic.mseed'

# 파일 읽기
stream = obspy.read(file_path)

# 스트림 정보 출력
print("Stream Information:")
print(stream)

# 각 트레이스의 정보 출력
for i, trace in enumerate(stream):
    print(f"\nTrace {i} Information:")
    print(trace)
    print(trace.stats)  # 트레이스 메타데이터 출력 (샘플링 속도, 시작 시간 등)
    print("First 10 data points:", trace.data[:10])  # 진폭 데이터 일부 미리보기
