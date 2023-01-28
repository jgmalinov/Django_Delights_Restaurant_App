from django.test import TestCase
from restaurant.models import MenuItem, Ingredient, RecipeRequirement
from restaurant.views import MenuItemCreate
from django.urls import reverse
from decimal import Decimal
from django.contrib.auth.models import User
# Create your tests here.

class MenuItemTestCase(TestCase):
    def setUp(self):
        MenuItem.objects.create(name='pizza', price=4.9)
        Ingredient.objects.create(name='tomato sauce', price=2.2, quantity_available=0.3, metric="L")
        pizza = MenuItem.objects.get(name='pizza')
        tomato_sauce = Ingredient.objects.get(name='tomato sauce')
        RecipeRequirement.objects.create(ingredient_id=tomato_sauce, menu_item_id=pizza, quantity_needed=0.1)

    def test_menu_item_exists(self):
        pizza = MenuItem.objects.get(name='pizza')
        self.assertIsInstance(pizza, MenuItem)
        self.assertEqual(pizza.name, 'pizza')
        self.assertEqual(pizza.price, Decimal('4.9'))
    
    def test_menu_item_is_correctly_referenced(self):
        pizza = MenuItem.objects.get(name='pizza')
        pizza_requirements = RecipeRequirement.objects.filter(menu_item_id = pizza)
        self.assertEqual(pizza, pizza_requirements[0].menu_item_id)
    
    def test_menu_item_cost_is_calculated_correctly(self):
        pizza = MenuItem.objects.get(name='pizza')
        tomato_sauce = Ingredient.objects.get(name='tomato sauce')
        tomato_sauce_requirement = RecipeRequirement.objects.filter(menu_item_id = pizza)[0]
        self.assertEqual(pizza.get_cost(), tomato_sauce.price * tomato_sauce_requirement.quantity_needed)


class CreateMenuItemViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ivan', password='Ivan1234')
        self.client.login(username='ivan', password='Ivan1234')


    def test_view_exists_at_url(self):
        response = self.client.get('/accounts/menu/create')
        self.assertEqual(response.status_code, 200)

    def test_view_exists_at_url_by_name(self):
        response = self.client.get(reverse('menu_create'))
        self.assertEqual(response.status_code, 200)

    def test_view_utilizes_intended_template(self):
        response = self.client.get(reverse('menu_create'))
        self.assertTemplateUsed(response, 'restaurant/menuitem_create.html')

    def test_view_creates_menu_item_on_valid_post(self):
        response = self.client.post(reverse('menu_create'), {'name': 'chicken soup', 'price': '1.99', \
            'radio1': 'NewIngredient', 'ingredient1': 'chicken', 'quantity1': '0.25', 'metric1': 'KG', 'price1': '1'})
        
        menu_item = MenuItem.objects.get(name='chicken soup')
        self.assertIsInstance(menu_item, MenuItem)
        self.assertEqual(menu_item.name, 'chicken soup')
        self.assertEqual(menu_item.price, Decimal('1.99'))

    def test_view_creates_ingredient_on_valid_post(self):
        response = self.client.post(reverse('menu_create'), {'name': 'chicken soup', 'price': '1.99', \
            'radio1': 'NewIngredient', 'ingredient1': 'chicken', 'quantity1': '0.25', 'metric1': 'KG', 'price1': '1'})
        
        ingredient = Ingredient.objects.get(name='chicken')
        self.assertIsInstance(ingredient, Ingredient)
        self.assertEqual(ingredient.name, 'chicken')
        self.assertEqual(ingredient.price, Decimal('1'))
        self.assertEqual(ingredient.quantity_available, Decimal('0.00'))
    
    def test_view_creates_recipe_requirement_on_valid_post(self):
        response = self.client.post(reverse('menu_create'), {'name': 'chicken soup', 'price': '1.99', \
            'radio1': 'NewIngredient', 'ingredient1': 'chicken', 'quantity1': '0.25', 'metric1': 'KG', 'price1': '1'})

        menu_item = MenuItem.objects.get(name='chicken soup')
        ingredient = Ingredient.objects.get(name='chicken')
        
        recipe_requirement = RecipeRequirement.objects.get(menu_item_id=menu_item, ingredient_id=ingredient)
        self.assertIsInstance(recipe_requirement, RecipeRequirement)
        self.assertEqual(recipe_requirement.quantity_needed, Decimal('0.25'))
    
    def test_view_contains_success_message_on_valid_post(self):
        response = self.client.post(reverse('menu_create'), {'name': 'chicken soup', 'price': '1.99', \
            'radio1': 'NewIngredient', 'ingredient1': 'chicken', 'quantity1': '0.25', 'metric1': 'KG', 'price1': '1'})
        
        self.assertContains(response, 'Menu item successfully added!')
    
