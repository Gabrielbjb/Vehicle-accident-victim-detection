def proses_deteksi_kecelakaan(lokasifile):
    from ultralytics import YOLO
    import os
    import cv2
    # Memuat model YOLOv8
    model = YOLO('model.pt') 
    namafile = lokasifile.split("/")[-1::][0].split(".")[0]
    # Menentukan folder tujuan untuk menyimpan hasil
    output_folder = '/static/selesai'  # Folder untuk menyimpan hasil ke /static/selesai
    os.makedirs(output_folder, exist_ok=True)
    apakah_ada = False

    print(lokasifile)
    # Cek apakah input adalah video atau gambar
    if lokasifile.lower().endswith(('.png', '.jpg', '.jpeg')):
        # Memproses gambar
        frame = cv2.imread(lokasifile)
        results = model(frame) 
        frame_with_results = results[0].plot()
        output_image_path = os.path.join(os.getcwd(), 'static', 'selesai', f"{namafile}.png")
        cv2.imwrite(output_image_path, frame_with_results)  # Simpan hasil sebagai gambar
        for result in results[0].boxes:
            if result.cls != None: 
                apakah_ada = True
                break
        format = ".png"

    elif lokasifile.lower().endswith(('.mp4', '.avi', '.mov')): 
        # Memproses video
        cap = cv2.VideoCapture(lokasifile)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Ganti 'mp4v' dengan 'avc1' untuk codec H.264
        output_video_path = os.path.join(os.getcwd(), 'static', 'selesai', f"{namafile}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'avc1')  # Menggunakan codec H.264
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            results = model(frame)
            frame_with_results = results[0].plot()
            out.write(frame_with_results)

            if not apakah_ada:
                for result in results[0].boxes:
                    if result.cls != None: 
                        apakah_ada = True
                        break
        cap.release()
        out.release()
        format = "mp4"

    if apakah_ada:
        return ["Kecelakaan Terdeteksi", "Kami mendeteksi ada kejadian kecelakaan di foto atau video yang anda unggah!", f"{namafile}.{format}"]
    else:    
        return ["Tidak Ada Kecelakaan", "Kami tidak mendeteksi ada kejadian kecelakaan di foto atau video yang anda unggah!", f"{namafile}.{format}"]
