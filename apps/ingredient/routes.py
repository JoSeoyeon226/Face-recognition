from apps.ingredient import blueprint
from flask_login import login_required
from flask import render_template, request, redirect, url_for
from apps.ingredient.models import Ingredient
from apps.ingredient.forms import IngredientForm
from datetime import datetime
from apps import db


# 목록
@blueprint.route('/ingredient_list')
@login_required
def ingredient_list():
    ingredient_list = Ingredient.query.all()
    return render_template('ingredient/list.html', ingredient_list=ingredient_list)


# 등록
@blueprint.route('/ingredient_create', methods=["GET", "POST"])
@login_required
def ingredient_create():
    form = IngredientForm(request.form)
    if request.method == "POST":
    #if form.validate_on_submit():
        ingredient = Ingredient()
        ingredient.ingredient = form.ingredient.data
        db.session.add(ingredient)
        db.session.commit()
        return redirect(url_for('ingredient_blueprint.ingredient_list'))
    return render_template('ingredient/create.html', form=form)


# 보기
@blueprint.route('/ingredient_read')
@login_required
def ingredient_read():
    return 'ingredient_read'


# 수정
@blueprint.route('/ingredient_update/<ingredient_id>', methods=["GET", "POST"])
@login_required
def ingredient_update(ingredient_id):
    ingredient = Ingredient.query.filter_by(id=ingredient_id).first()
    form = IngredientForm(request.form)
    if request.method == "POST":
        # if form.validate_on_submit():
        ingredient.ingredient = form.ingredient.data
        db.session.commit()
        return redirect(url_for('ingredient_blueprint.ingredient_list'))
    return render_template('ingredient/update.html', ingredient=ingredient, form=form)


# 삭제
@blueprint.route('/ingredient_delete/<ingredient_id>')
@login_required
def ingredient_delete(ingredient_id):
    Ingredient.query.filter_by(id=ingredient_id).delete()
    db.session.commit()
    return redirect(url_for('ingredient_blueprint.ingredient_list'))

