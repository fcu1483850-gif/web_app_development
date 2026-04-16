from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import RecordModel

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    records = RecordModel.get_all()
    # 計算總收入、總支出與餘額
    total_income = sum(r['amount'] for r in records if r['type'] == 'income')
    total_expense = sum(r['amount'] for r in records if r['type'] == 'expense')
    balance = total_income - total_expense
    return render_template('index.html', records=records, balance=balance, income=total_income, expense=total_expense)

@bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        type_ = request.form.get('type')
        category = request.form.get('category')
        amount_str = request.form.get('amount')
        date = request.form.get('date')
        description = request.form.get('description', '')
        
        try:
            amount = float(amount_str)
            if amount < 0: raise ValueError
        except (TypeError, ValueError):
            flash('金額格式錯誤或必須大於 0', 'danger')
            return redirect(url_for('routes.add'))
            
        if not all([type_, category, amount_str, date]):
            flash('請填寫所有必填欄位', 'danger')
            return redirect(url_for('routes.add'))
            
        RecordModel.create(type_, category, amount, date, description)
        flash('新增紀錄成功！', 'success')
        return redirect(url_for('routes.index'))
    return render_template('form.html', record=None)

@bp.route('/edit/<int:record_id>', methods=['GET', 'POST'])
def edit(record_id):
    record = RecordModel.get_by_id(record_id)
    if not record:
        flash('找不到該筆紀錄', 'danger')
        return redirect(url_for('routes.index'))
        
    if request.method == 'POST':
        type_ = request.form.get('type')
        category = request.form.get('category')
        amount_str = request.form.get('amount')
        date = request.form.get('date')
        description = request.form.get('description', '')
        
        try:
            amount = float(amount_str)
            if amount < 0: raise ValueError
        except (TypeError, ValueError):
            flash('金額格式錯誤或必須大於 0', 'danger')
            return redirect(url_for('routes.edit', record_id=record_id))
            
        if not all([type_, category, amount_str, date]):
            flash('請填寫所有必填欄位', 'danger')
            return redirect(url_for('routes.edit', record_id=record_id))
            
        RecordModel.update(record_id, type_, category, amount, date, description)
        flash('紀錄更新成功！', 'success')
        return redirect(url_for('routes.index'))
        
    return render_template('form.html', record=record)

@bp.route('/delete/<int:record_id>', methods=['POST'])
def delete(record_id):
    RecordModel.delete(record_id)
    flash('紀錄已成功刪除', 'success')
    return redirect(url_for('routes.index'))
