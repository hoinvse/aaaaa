from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from pytz import timezone

app = Flask(__name__)

# Danh sách tạm thời để lưu trữ giao dịch
danh_sach_giao_dich = []

# Model cho giao dịch
class GiaoDich:
    def __init__(self, id, mo_ta, so_tien, loai, ngay_tao):
        self.id = id
        self.mo_ta = mo_ta
        self.so_tien = so_tien
        self.loai = loai
        self.ngay_tao = ngay_tao

# Route chính
@app.route('/')
def index():
    thang_hien_tai = int(request.args.get('thang', datetime.now().month))
    giao_dich = [gd for gd in danh_sach_giao_dich if gd.ngay_tao.month == thang_hien_tai]

    tong_thu_nhap = sum(gd.so_tien for gd in giao_dich if gd.loai == 'thu_nhap')
    tong_chi_phi = sum(gd.so_tien for gd in giao_dich if gd.loai == 'chi_phi')

    # Chuyển múi giờ thành Hồ Chí Minh (GMT+7)
    vn_tz = timezone('Asia/Ho_Chi_Minh')
    for gd in giao_dich:
        gd.ngay_tao = gd.ngay_tao.replace(tzinfo=timezone('UTC')).astimezone(vn_tz).strftime("%d/%m/%Y %H:%M:%S")
    
    return render_template('index.html', giao_dich=giao_dich, tong_thu_nhap=tong_thu_nhap, tong_chi_phi=tong_chi_phi, thang_hien_tai=thang_hien_tai)

# Route thêm giao dịch
@app.route('/them', methods=['GET', 'POST'])
def them_giao_dich():
    if request.method == 'POST':
        mo_ta = request.form['mo_ta']
        so_tien = float(request.form['so_tien'])
        loai = request.form['loai']
        ngay_tao = datetime.utcnow()
        
        # Tạo một đối tượng GiaoDich và thêm vào danh sách tạm thời
        gd = GiaoDich(len(danh_sach_giao_dich) + 1, mo_ta, so_tien, loai, ngay_tao)
        danh_sach_giao_dich.append(gd)
        
        return redirect(url_for('index'))
    return render_template('themgiaodich.html')

# Route xóa giao dịch
@app.route('/xoa/<int:id>')
def xoa_giao_dich(id):
    global danh_sach_giao_dich
    danh_sach_giao_dich = [gd for gd in danh_sach_giao_dich if gd.id != id]
    return redirect(url_for('index'))

# Route cập nhật giao dịch
@app.route('/cap_nhat/<int:id>', methods=['GET', 'POST'])
def cap_nhat_giao_dich(id):
    gd = next((gd for gd in danh_sach_giao_dich if gd.id == id), None)
    if gd is None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        gd.mo_ta = request.form['mo_ta']
        gd.so_tien = float(request.form['so_tien'])
        gd.loai = request.form['loai']
        return redirect(url_for('index'))
    else:
        return render_template('cap_nhat.html', gd=gd)

if __name__ == '__main__':
    app.run(debug=True)
