query_check = """
            SELECT status FROM jadwalkegiatan where id_kegiatan = %s and nim = %s;
"""
            curse.execute(query_check,(id_kegiatan,self.username))
            ceksttus = curse.fetchone()
            # ini mengek apakah id_kegiatan tersebut sudah dikumpulkan didalam daftarkegiatanselesai
            sudah_selesai =  ceksttus and ceksttus [0] == 'selesai'  #ini mengecek jika lebih dari 1 maka sudah seesai

            # menghilangkan pengingat jika batasnya sudah melewati deadline
            if sisaHari < 0 or sudah_selesai:
                continue

            # deadline hari ini
            elif sisaHari == 0:
                pesan = f"Kegiatan '{namajudul}' harus diselesaikan hari ini ({formatDeadline.toString('dd MMMM yyyy HH:mm:ss')})!"
                QMessageBox.warning(self, "Deadline Hari Ini", pesan)

            # tenggal hari <= 3 hari
            elif sisaHari <= 3:
                pesan = f"Kegiatan '{namajudul}' akan jatuh tempo dalam {sisaHari} hari, yaitu pada {formatDeadline.toString('dd MMMM yyyy HH:mm:ss')}."
                QMessageBox.information(self, "Pengingat Deadline", pesan)