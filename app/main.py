from flask import Flask, render_template, request
from wtforms import StringField, SubmitField
from flask.views import MethodView
from flask_wtf import FlaskForm
from inci.ingredient_group import IngredientGroup
from inci.ingredient import Ingredient
from inci.inci_function import INCIFunction
from inci.abbreviation import Abbreviation
from inci.pdf_generator import PdfGenerator
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['APP_KEY']


class HomePage(MethodView):

    def get(self):
        return render_template("index.html")


class MainSearchPage(MethodView):

    def get(self):
        main_search = IngredientsForm()
        return render_template("main-search.html",
                               mainsearch=main_search)


class IngredientsResultPage(MethodView):

    def get(self):
        one_search = OneIngredientForm(request.form)
        return render_template("ingredients-result.html",
                               onesearch=one_search,
                               result=True)

    def post(self):
        main_search = IngredientsForm(request.form)
        ingredients = IngredientGroup(main_search.incis.data.strip()).\
            show_ingredients()

        one_search = OneIngredientForm(request.form)
        ingredient = Ingredient(one_search.inci.data.strip()).\
            show_description()
        inci_func = Ingredient(one_search.inci.data).show_function()

        inci_pdf = ""
        for i in ingredients:
            inci_pdf = inci_pdf + i + ", "

        pdf = PdfGenerator(str(inci_pdf))
        pdf.create()
        link = pdf.share()

        if ingredients == "Type at least 3 characters. Try again!" or \
                ingredients == "No search results. Try again!":
            return render_template("try-again.html",
                                   ingredients=ingredients)

        return render_template("ingredients-result.html",
                               mainsearch=main_search,
                               onesearch=one_search,
                               ingredient=ingredient,
                               ingredients=ingredients,
                               incifunc=inci_func,
                               link=link,
                               result=True)


class OneIngredientPage(MethodView):

    def get(self):
        one_search = OneIngredientForm(request.form)
        return render_template("one-ingredient.html",
                               onesearch=one_search,)

    def post(self):
        one_search = OneIngredientForm(request.form)
        ingredient = Ingredient(one_search.inci.data.strip()).\
            show_description()

        inci_func = Ingredient(one_search.inci.data.strip()).show_function()
        func_search = IngFuncForm(request.form)
        func_name = INCIFunction(func_search.func_name.data.strip()).\
            show_info()

        inci_pdf = ""
        for i in ingredient:
            inci_pdf = inci_pdf + "\n" + i

        pdf = PdfGenerator(inci_pdf)
        pdf.create()
        link = pdf.share()

        if ingredient == f"It seems we don't have this ingredient " \
                         f"in our database. Try again!":
            return render_template("try-again.html",
                                   ingredient=ingredient)

        return render_template("one-ingredient.html",
                               onesearch=one_search,
                               ingredient=ingredient,
                               funcsearch=func_search,
                               incifunc=inci_func,
                               funcname=func_name,
                               link=link,
                               result=True)


class IngFuncPage(MethodView):

    def post(self):
        one_search = OneIngredientForm(request.form)
        ingredient = Ingredient(one_search.inci.data.strip()).\
            show_description()

        func_search = IngFuncForm(request.form)
        func_name = INCIFunction(func_search.func_name.data.strip()).\
            show_info()

        if func_name == "Type at least 3 characters. Try again!" or \
                func_name == "It seems we don't have " \
                             "this function in our database. Try again!":
            return render_template("try-again.html",
                                   funcname=func_name)

        return render_template("inci-func.html",
                               onesearch=one_search,
                               ingredient=ingredient,
                               funcsearch=func_search,
                               funcname=func_name,
                               result=True)


class FunctionSearchPage(MethodView):

    def get(self):
        func_form = FuncForm()
        return render_template("function-search.html",
                               funcform=func_form)

    def post(self):
        func_form = FuncForm(request.form)
        func_info = INCIFunction(func_form.func_name.data.strip()).show_info()

        return render_template("function-search.html",
                               funcform=func_form,
                               funcinfo=func_info,
                               result=True)


class AbbrevSearchPage(MethodView):

    def get(self):
        abbrev_form = AbbrevForm()
        return render_template("abbrev-search.html",
                               abbrevform=abbrev_form)

    def post(self):
        abbrev_form = AbbrevForm()
        abbrev_info = Abbreviation(abbrev_form.abbrev_name.data.strip()).show_abbrev_in()

        return render_template("abbrev-search.html",
                               abbrevform=abbrev_form,
                               abbrevinfo=abbrev_info,
                               result=True)


class AboutDBPage(MethodView):

    def get(self):
        return render_template("cosing-database.html")


class AboutMe(MethodView):

    def get(self):
        return render_template("about.html")


class IngredientsForm(FlaskForm):

    incis = StringField()
    button = SubmitField("Search")


class OneIngredientForm(FlaskForm):

    inci = StringField()
    button = SubmitField("Search")


class IngFuncForm(FlaskForm):

    func_name = StringField()
    button = SubmitField("Search")


class FuncForm(FlaskForm):

    func_name = StringField()
    button = SubmitField("Search")


class AbbrevForm(FlaskForm):

    abbrev_name = StringField()
    button = SubmitField("Search")


app.add_url_rule("/", view_func=HomePage.as_view("home_page"))
app.add_url_rule("/main-search",
                 view_func=MainSearchPage.as_view("main_search_page"))
app.add_url_rule("/ingredients-result",
                 view_func=IngredientsResultPage.as_view
                 ("ingredients_result_page"))
app.add_url_rule("/one-ingredient",
                 view_func=OneIngredientPage.as_view("one_ingredient_page"))
app.add_url_rule("/inci-func",
                 view_func=IngFuncPage.as_view("inci_func_page"))
app.add_url_rule("/function-search",
                 view_func=FunctionSearchPage.as_view("func_search_page"))
app.add_url_rule("/abbrev-search",
                 view_func=AbbrevSearchPage.as_view("abbrev_search_page"))
app.add_url_rule("/cosing-database",
                 view_func=AboutDBPage.as_view("about_db_page"))
app.add_url_rule("/about",
                 view_func=AboutMe.as_view("about"))

app.run(debug=True)
