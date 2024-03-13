import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from unittest.mock import patch

from .test_recipes_base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeIndexFunctionalTest(RecipeBaseFunctionalTest):

    def test_recipe_index_page_without_recipes(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn(
            'No momento não tem-se receitas', body.text
        )

    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_index_page_search_can_find_correct_recipes(self):
        self.make_recipe_in_batch()

        # Abertura da pg
        self.browser.get(self.live_server_url)

        # Ve o campo de busca com o Texto: "Pesquisar receitas"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Pesquisar receitas"]'
        )

        # clica neste input e digita o termo de busca
        # para encontrar a receita com esse titulo
        search_input.send_keys('Recipe Title 1')
        search_input.send_keys(Keys.ENTER)

        self.assertIn(
            'Recipe Title 1',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    @patch('recipes.views.site.PER_PAGE', new=3)
    def test_recipe_index_page_pagination(self):
        self.make_recipe_in_batch(qtd=15)
        # Abertura da pg

        self.browser.get(self.live_server_url)

        # ve que tem paginaçao e clica na pagina 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="va para pagina 2"]'
        )

        page2.click()

        # ve que tem mais 3 receitas na pg 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            3
        )
