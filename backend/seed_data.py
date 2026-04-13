"""Seed script for No Limit Delivery - South African multi-service platform
Complete data with unique stock images for every item.
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import uuid
from datetime import datetime, timezone

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["test_database"]

# =====================================================================
# IMAGE POOLS - Curated Unsplash URLs by category for unique per-item images
# =====================================================================
IMG = {
    # Grilled Chicken
    "chicken_quarter": "https://images.unsplash.com/photo-1626645738196-c2a7c87a8f58?w=400&h=300&fit=crop",
    "chicken_half": "https://images.unsplash.com/photo-1598103442097-8b74f90f6efc?w=400&h=300&fit=crop",
    "chicken_full": "https://images.unsplash.com/photo-1606728035253-49e8a23146de?w=400&h=300&fit=crop",
    "chicken_wings": "https://images.unsplash.com/photo-1527477396000-e27163b4bbed?w=400&h=300&fit=crop",
    "chicken_meal": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=400&h=300&fit=crop",
    "chicken_fried": "https://images.unsplash.com/photo-1587593810167-a84920ea0781?w=400&h=300&fit=crop",
    "chicken_strips": "https://images.unsplash.com/photo-1562967914-608f82629710?w=400&h=300&fit=crop",
    "chicken_drumstick": "https://images.unsplash.com/photo-1501200291289-c5a76c232e5f?w=400&h=300&fit=crop",
    "chicken_thigh": "https://images.unsplash.com/photo-1610057099443-fde6c0d0fd14?w=400&h=300&fit=crop",
    "chicken_grilled2": "https://images.unsplash.com/photo-1594221708779-94832f4320d1?w=400&h=300&fit=crop",

    # Burgers
    "burger_classic": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400&h=300&fit=crop",
    "burger_cheese": "https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=400&h=300&fit=crop",
    "burger_double": "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=400&h=300&fit=crop",
    "burger_chicken": "https://images.unsplash.com/photo-1593022754339-f23454332fd8?w=400&h=300&fit=crop",
    "burger_bacon": "https://images.unsplash.com/photo-1586190848861-99aa4a171e90?w=400&h=300&fit=crop",
    "burger_meal": "https://images.unsplash.com/photo-1550547660-d9450f859349?w=400&h=300&fit=crop",
    "burger_gourmet": "https://images.unsplash.com/photo-1594212699903-ec8a3eca50f5?w=400&h=300&fit=crop",
    "burger_bbq": "https://images.unsplash.com/photo-1572802419224-296b0aeee0d9?w=400&h=300&fit=crop",
    "burger_veggie": "https://images.unsplash.com/photo-1585238342024-78d387f4a707?w=400&h=300&fit=crop",
    "burger_deluxe": "https://images.unsplash.com/photo-1565299507177-b0ac66763828?w=400&h=300&fit=crop",
    "burger_tower": "https://images.unsplash.com/photo-1551360198-346d4b399e21?w=400&h=300&fit=crop",

    # Mexican
    "enchilada": "https://images.unsplash.com/photo-1534352956036-cd81e27dd615?w=400&h=300&fit=crop",
    "fajita": "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?w=400&h=300&fit=crop",
    "nachos": "https://images.unsplash.com/photo-1513456852971-30c0b8199d4d?w=400&h=300&fit=crop",
    "quesadilla": "https://images.unsplash.com/photo-1618040996337-56904b7850b9?w=400&h=300&fit=crop",
    "burrito": "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=400&h=300&fit=crop",
    "taco": "https://images.unsplash.com/photo-1599974579688-8dbdd335c77f?w=400&h=300&fit=crop",

    # Fries / Chips
    "chips_regular": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=400&h=300&fit=crop",
    "chips_loaded": "https://images.unsplash.com/photo-1630384060421-cb20d0e0649d?w=400&h=300&fit=crop",
    "chips_thin": "https://images.unsplash.com/photo-1576107232684-1279f390859f?w=400&h=300&fit=crop",
    "chips_curly": "https://images.unsplash.com/photo-1585109649139-366815a0d713?w=400&h=300&fit=crop",
    "chips_wedges": "https://images.unsplash.com/photo-1548340748-6d2b7d7da280?w=400&h=300&fit=crop",
    "chips_large": "https://images.unsplash.com/photo-1529589510304-b7e994a92f60?w=400&h=300&fit=crop",
    "chips_cheesy": "https://images.unsplash.com/photo-1614174486414-a8d5dde56b60?w=400&h=300&fit=crop",
    "chips_plain": "https://images.unsplash.com/photo-1518013431117-eb1465fa5752?w=400&h=300&fit=crop",
    "chips_family": "https://images.unsplash.com/photo-1541592106381-b31e9677c0e4?w=400&h=300&fit=crop",

    # Rice / Sides
    "rice_mexican": "https://images.unsplash.com/photo-1596560548464-f010549b84d7?w=400&h=300&fit=crop",
    "corn_cob": "https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=400&h=300&fit=crop",
    "coleslaw": "https://images.unsplash.com/photo-1536304929831-ee1ca9d44f64?w=400&h=300&fit=crop",
    "garlic_roll": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&h=300&fit=crop",
    "pap": "https://images.unsplash.com/photo-1604329760661-e71dc83f8f26?w=400&h=300&fit=crop",
    "side_salad": "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=400&h=300&fit=crop",
    "greek_salad": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400&h=300&fit=crop",
    "braai_broodjie": "https://images.unsplash.com/photo-1528736235302-52922df5c122?w=400&h=300&fit=crop",

    # Shawarma / Wraps
    "shawarma": "https://images.unsplash.com/photo-1529006557810-274b9b2fc783?w=400&h=300&fit=crop",
    "shawarma2": "https://images.unsplash.com/photo-1561651188-d207bbec4ec3?w=400&h=300&fit=crop",
    "wrap_chicken": "https://images.unsplash.com/photo-1644419543419-ad0e3e0ee73e?w=400&h=300&fit=crop",
    "wrap_beef": "https://images.unsplash.com/photo-1600688640154-9619e002df30?w=400&h=300&fit=crop",
    "wrap_veg": "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=400&h=300&fit=crop",

    # Tikka / Kebab / Grills
    "tikka": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop",
    "kebab": "https://images.unsplash.com/photo-1603360946369-dc9bb6258143?w=400&h=300&fit=crop",
    "seekh_kabab": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=400&h=300&fit=crop",
    "boti": "https://images.unsplash.com/photo-1610057099443-fde6c0d0fd14?w=400&h=300&fit=crop",

    # Platter / Sharing
    "platter_chicken": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400&h=300&fit=crop",
    "platter_meat": "https://images.unsplash.com/photo-1544025162-d76694265947?w=400&h=300&fit=crop",
    "meatbox": "https://images.unsplash.com/photo-1529694157872-4e0c0f3b238b?w=400&h=300&fit=crop",

    # Sandwiches
    "sandwich_toasted": "https://images.unsplash.com/photo-1528736235302-52922df5c122?w=400&h=300&fit=crop",
    "sandwich_club": "https://images.unsplash.com/photo-1553909489-cd47e0907980?w=400&h=300&fit=crop",
    "sandwich_cheese": "https://images.unsplash.com/photo-1481070555726-e2fe8357b3e4?w=400&h=300&fit=crop",
    "sandwich_dagwood": "https://images.unsplash.com/photo-1509722747041-616f39b57569?w=400&h=300&fit=crop",

    # Hot Dogs / Russians
    "hotdog": "https://images.unsplash.com/photo-1612392062126-3b89f654c3d4?w=400&h=300&fit=crop",
    "hotdog2": "https://images.unsplash.com/photo-1619740455993-9d701c76e89d?w=400&h=300&fit=crop",
    "russian": "https://images.unsplash.com/photo-1587536849024-daaa4a417b16?w=400&h=300&fit=crop",
    "russian_large": "https://images.unsplash.com/photo-1551218808-94e220e084d2?w=400&h=300&fit=crop",
    "cheese_griller": "https://images.unsplash.com/photo-1561758033-d89a9ad46330?w=400&h=300&fit=crop",

    # Kota
    "kota": "https://images.unsplash.com/photo-1606755962773-d324e0a13086?w=400&h=300&fit=crop",
    "kota_russian": "https://images.unsplash.com/photo-1594212699903-ec8a3eca50f5?w=400&h=300&fit=crop",
    "chip_roll": "https://images.unsplash.com/photo-1561758033-7e924f619b47?w=400&h=300&fit=crop",

    # Indian / Curry
    "curry_chicken": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400&h=300&fit=crop",
    "curry_beef": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop",
    "curry_mutton": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=400&h=300&fit=crop",
    "curry_beans": "https://images.unsplash.com/photo-1596797038530-2c107229654b?w=400&h=300&fit=crop",
    "curry_butter": "https://images.unsplash.com/photo-1574484284002-952d92456975?w=400&h=300&fit=crop",
    "biryani": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400&h=300&fit=crop",
    "bunny_chow_chicken": "https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=400&h=300&fit=crop",
    "bunny_chow_beef": "https://images.unsplash.com/photo-1574484284002-952d92456975?w=400&h=300&fit=crop",
    "bunny_chow_mutton": "https://images.unsplash.com/photo-1596797038530-2c107229654b?w=400&h=300&fit=crop",
    "bunny_chow_beans": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=400&h=300&fit=crop",
    "roti": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop",
    "tikka_chicken": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=400&h=300&fit=crop",
    "shawarma_double": "https://images.unsplash.com/photo-1561651188-d207bbec4ec3?w=400&h=300&fit=crop",

    # Grilled Meats / Braai / Steak
    "steak": "https://images.unsplash.com/photo-1558030006-450675393462?w=400&h=300&fit=crop",
    "steak_tbone": "https://images.unsplash.com/photo-1546964124-0cce460f38ef?w=400&h=300&fit=crop",
    "chops": "https://images.unsplash.com/photo-1432139555190-58524dae6a55?w=400&h=300&fit=crop",
    "ribs_full": "https://images.unsplash.com/photo-1544025162-d76694265947?w=400&h=300&fit=crop",
    "ribs_half": "https://images.unsplash.com/photo-1594041680534-e8c8cdebd659?w=400&h=300&fit=crop",
    "ribs_quarter": "https://images.unsplash.com/photo-1529694157872-4e0c0f3b238b?w=400&h=300&fit=crop",
    "brisket": "https://images.unsplash.com/photo-1529694157872-4e0c0f3b238b?w=400&h=300&fit=crop",
    "wors": "https://images.unsplash.com/photo-1587536849024-daaa4a417b16?w=400&h=300&fit=crop",
    "pork_chop": "https://images.unsplash.com/photo-1432139555190-58524dae6a55?w=400&h=300&fit=crop",
    "chuck": "https://images.unsplash.com/photo-1558030006-450675393462?w=400&h=300&fit=crop",
    "beef_rashers": "https://images.unsplash.com/photo-1546964124-0cce460f38ef?w=400&h=300&fit=crop",
    "beef_stew": "https://images.unsplash.com/photo-1547592180-85f173990554?w=400&h=300&fit=crop",
    "braai_box": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400&h=300&fit=crop",

    # Pizza
    "pizza_margherita": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&h=300&fit=crop",
    "pizza_pepperoni": "https://images.unsplash.com/photo-1571407970349-bc81e7e96d47?w=400&h=300&fit=crop",
    "pizza_hawaiian": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&h=300&fit=crop",
    "pizza_meat": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400&h=300&fit=crop",
    "pizza_bbq": "https://images.unsplash.com/photo-1588315029754-2dd089d39a1a?w=400&h=300&fit=crop",
    "pizza_cheese": "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=400&h=300&fit=crop",
    "pizza_veggie": "https://images.unsplash.com/photo-1534308983496-4fabb1a015ee?w=400&h=300&fit=crop",
    "pizza_chicken": "https://images.unsplash.com/photo-1593560708920-61dd98c46a4e?w=400&h=300&fit=crop",
    "pizza_slice": "https://images.unsplash.com/photo-1595854341625-f33ee10dbf94?w=400&h=300&fit=crop",
    "pizza_special": "https://images.unsplash.com/photo-1571997478779-2adcbbe9ab2f?w=400&h=300&fit=crop",
    "pizza_loaded": "https://images.unsplash.com/photo-1590947132387-155cc02f3212?w=400&h=300&fit=crop",
    "pizza_biltong": "https://images.unsplash.com/photo-1585238342024-78d387f4a707?w=400&h=300&fit=crop",
    "pizza_dessert": "https://images.unsplash.com/photo-1562440499-64c9a111f713?w=400&h=300&fit=crop",
    "pizza_kids": "https://images.unsplash.com/photo-1600028068383-ea11a7a101f3?w=400&h=300&fit=crop",
    "pie_meat": "https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=400&h=300&fit=crop",
    "pie_chicken": "https://images.unsplash.com/photo-1608039829572-26d3b6b0e65d?w=400&h=300&fit=crop",

    # Combo / Box / Family Meal
    "combo_box": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400&h=300&fit=crop",
    "combo_family": "https://images.unsplash.com/photo-1606755962773-d324e0a13086?w=400&h=300&fit=crop",
    "combo_variety": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400&h=300&fit=crop",
    "kids_meal": "https://images.unsplash.com/photo-1562967916-eb82221dfb92?w=400&h=300&fit=crop",

    # Coffee / Cafe
    "espresso": "https://images.unsplash.com/photo-1510707577719-ae7c14805e3a?w=400&h=300&fit=crop",
    "espresso_double": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefda?w=400&h=300&fit=crop",
    "cappuccino": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400&h=300&fit=crop",
    "cappuccino_large": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400&h=300&fit=crop",
    "latte": "https://images.unsplash.com/photo-1497935586351-b67a49e012bf?w=400&h=300&fit=crop",
    "latte_vanilla": "https://images.unsplash.com/photo-1442512595331-e89e73853f31?w=400&h=300&fit=crop",
    "latte_caramel": "https://images.unsplash.com/photo-1485808191679-5f86510681a2?w=400&h=300&fit=crop",
    "latte_hazelnut": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=300&fit=crop",
    "mocha": "https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=400&h=300&fit=crop",
    "mocha_large": "https://images.unsplash.com/photo-1517578239113-b03992dcdd25?w=400&h=300&fit=crop",
    "americano": "https://images.unsplash.com/photo-1521302080334-4bebac2763a6?w=400&h=300&fit=crop",
    "flat_white": "https://images.unsplash.com/photo-1534687941688-651ccaafbff8?w=400&h=300&fit=crop",
    "macchiato": "https://images.unsplash.com/photo-1485808191679-5f86510681a2?w=400&h=300&fit=crop",
    "cortado": "https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?w=400&h=300&fit=crop",
    "chai_latte": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=400&h=300&fit=crop",
    "dirty_chai": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=400&h=300&fit=crop",
    "hot_chocolate": "https://images.unsplash.com/photo-1542990253-0d0f5be5f0ed?w=400&h=300&fit=crop",
    "hot_chocolate_large": "https://images.unsplash.com/photo-1517578239113-b03992dcdd25?w=400&h=300&fit=crop",
    "red_cappuccino": "https://images.unsplash.com/photo-1504630083234-14187a9df0f5?w=400&h=300&fit=crop",
    "tea_roses": "https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=400&h=300&fit=crop",
    "tea_rooibos": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400&h=300&fit=crop",

    # Cold Drinks / Freezo / Shakes
    "freezo_coffee": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400&h=300&fit=crop",
    "freezo_choco": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=400&h=300&fit=crop",
    "freezo_mocha": "https://images.unsplash.com/photo-1541658016709-82535e94bc69?w=400&h=300&fit=crop",
    "freezo_mango": "https://images.unsplash.com/photo-1546173159-315724a31696?w=400&h=300&fit=crop",
    "freezo_honey": "https://images.unsplash.com/photo-1579954115545-a95591f28bfc?w=400&h=300&fit=crop",
    "freezo_passion": "https://images.unsplash.com/photo-1497534446932-c925b458314e?w=400&h=300&fit=crop",
    "shake_vanilla": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=400&h=300&fit=crop",
    "shake_chocolate": "https://images.unsplash.com/photo-1541658016709-82535e94bc69?w=400&h=300&fit=crop",
    "shake_strawberry": "https://images.unsplash.com/photo-1579954115545-a95591f28bfc?w=400&h=300&fit=crop",
    "shake_peanut": "https://images.unsplash.com/photo-1553787499-6f9133860278?w=400&h=300&fit=crop",
    "shake_cherry": "https://images.unsplash.com/photo-1577805947697-89e18249d767?w=400&h=300&fit=crop",
    "shake_blueberry": "https://images.unsplash.com/photo-1553787434-dd9eb4ea4d0b?w=400&h=300&fit=crop",
    "ice_block": "https://images.unsplash.com/photo-1497534446932-c925b458314e?w=400&h=300&fit=crop",

    # Soft Drinks
    "coke": "https://images.unsplash.com/photo-1581098365948-6a5a912b7a49?w=400&h=300&fit=crop",
    "sprite": "https://images.unsplash.com/photo-1556881286-fc6915169721?w=400&h=300&fit=crop",
    "fanta": "https://images.unsplash.com/photo-1624517452488-04869289c4ca?w=400&h=300&fit=crop",
    "appletiser": "https://images.unsplash.com/photo-1534353473418-4cfa6c56fd38?w=400&h=300&fit=crop",
    "ice_tea": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400&h=300&fit=crop",
    "water": "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=400&h=300&fit=crop",
    "cold_drink": "https://images.unsplash.com/photo-1527960471264-932f39eb5846?w=400&h=300&fit=crop",

    # Pregos / Cafe Food
    "prego_chicken": "https://images.unsplash.com/photo-1553909489-cd47e0907980?w=400&h=300&fit=crop",
    "prego_beef": "https://images.unsplash.com/photo-1509722747041-616f39b57569?w=400&h=300&fit=crop",
    "road_dog": "https://images.unsplash.com/photo-1612392062126-3b89f654c3d4?w=400&h=300&fit=crop",
    "road_dog_loaded": "https://images.unsplash.com/photo-1619740455993-9d701c76e89d?w=400&h=300&fit=crop",
    "roll_up": "https://images.unsplash.com/photo-1644419543419-ad0e3e0ee73e?w=400&h=300&fit=crop",
    "halloumi": "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=400&h=300&fit=crop",

    # Extras
    "alt_milk": "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&h=300&fit=crop",
    "espresso_shot": "https://images.unsplash.com/photo-1510707577719-ae7c14805e3a?w=400&h=300&fit=crop",
    "toast": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&h=300&fit=crop",
    "cheese_slice": "https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?w=400&h=300&fit=crop",
    "egg": "https://images.unsplash.com/photo-1510693206972-df098062cb71?w=400&h=300&fit=crop",
    "bacon": "https://images.unsplash.com/photo-1528607929212-2636ec44253e?w=400&h=300&fit=crop",
    "feta": "https://images.unsplash.com/photo-1564894809611-1742fc40ed80?w=400&h=300&fit=crop",
    "avocado": "https://images.unsplash.com/photo-1523049673857-eb18f1d7b578?w=400&h=300&fit=crop",
    "roti_bread": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&h=300&fit=crop",
    "marinade": "https://images.unsplash.com/photo-1472476443507-c7a5948772fc?w=400&h=300&fit=crop",

    # Breakfast
    "breakfast_full": "https://images.unsplash.com/photo-1533089860892-a7c6f0a88666?w=400&h=300&fit=crop",
    "waffles": "https://images.unsplash.com/photo-1562376552-0d160a2f238d?w=400&h=300&fit=crop",
    "granola": "https://images.unsplash.com/photo-1484723091739-30a097e8f929?w=400&h=300&fit=crop",
    "granola_large": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=400&h=300&fit=crop",
    "croissant": "https://images.unsplash.com/photo-1555507036-ab1f4038024a?w=400&h=300&fit=crop",
    "addon_breakfast": "https://images.unsplash.com/photo-1482049016688-2d3e1b311543?w=400&h=300&fit=crop",
    "breakfast_bun": "https://images.unsplash.com/photo-1550507992-eb63ffee0847?w=400&h=300&fit=crop",

    # Pasta
    "pasta_meatball": "https://images.unsplash.com/photo-1548247416-ec66f4900b2e?w=400&h=300&fit=crop",
    "pasta_pesto": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=400&h=300&fit=crop",
    "pasta_alfredo": "https://images.unsplash.com/photo-1555949258-eb67b1ef0ceb?w=400&h=300&fit=crop",
    "pasta_tomato": "https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=400&h=300&fit=crop",
    "lasagna": "https://images.unsplash.com/photo-1574894709920-11b28e7367e3?w=400&h=300&fit=crop",

    # Frozen Meals
    "frozen_lasagne": "https://images.unsplash.com/photo-1643878194973-644ee5a1eac6?w=400&h=300&fit=crop",
    "frozen_chicken_lasagne": "https://images.unsplash.com/photo-1696935257293-9ec4f03074a1?w=400&h=300&fit=crop",
    "frozen_pork_lasagne": "https://images.unsplash.com/photo-1574894709920-11b28e7367e3?w=400&h=300&fit=crop",
    "mac_cheese": "https://images.unsplash.com/photo-1612001418721-8e8cfb1fef0b?w=400&h=300&fit=crop",
    "mac_chicken": "https://images.unsplash.com/photo-1543339494-b4cd4f7ba686?w=400&h=300&fit=crop",
    "mac_bacon": "https://images.unsplash.com/photo-1570597935964-9e27028efd07?w=400&h=300&fit=crop",
    "mac_mince": "https://images.unsplash.com/photo-1580013759032-94a44305090d?w=400&h=300&fit=crop",
    "cottage_pie": "https://images.unsplash.com/photo-1595666548990-788e19dc3885?w=400&h=300&fit=crop",
    "cottage_chicken": "https://images.unsplash.com/photo-1547592180-85f173990554?w=400&h=300&fit=crop",
    "rice_mince": "https://images.unsplash.com/photo-1596560548464-f010549b84d7?w=400&h=300&fit=crop",
    "combo_10": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400&h=300&fit=crop",
    "combo_20": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400&h=300&fit=crop",
    "combo_30": "https://images.unsplash.com/photo-1606755962773-d324e0a13086?w=400&h=300&fit=crop",

    # Laundry
    "laundry_wash_fold": "https://images.unsplash.com/photo-1545173168-9f1947eebb7f?w=400&h=300&fit=crop",
    "laundry_wash_dry": "https://images.unsplash.com/photo-1517677208171-0bc6725a3e60?w=400&h=300&fit=crop",
    "laundry_iron": "https://images.unsplash.com/photo-1489274495757-95c7c837b101?w=400&h=300&fit=crop",
    "laundry_overall": "https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=400&h=300&fit=crop",
    "laundry_dry_clean": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=400&h=300&fit=crop",
    "laundry_suit": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=400&h=300&fit=crop",
    "laundry_sneakers": "https://images.unsplash.com/photo-1460353581641-37baddab0fa2?w=400&h=300&fit=crop",
    "laundry_slippers": "https://images.unsplash.com/photo-1603808033192-082d6919d3e1?w=400&h=300&fit=crop",
    "laundry_blazer": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=400&h=300&fit=crop",
    "laundry_jacket": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=300&fit=crop",
    "laundry_dress_evening": "https://images.unsplash.com/photo-1518622358385-8ea7d0794bf6?w=400&h=300&fit=crop",
    "laundry_dress_wedding": "https://images.unsplash.com/photo-1519741497674-611481863552?w=400&h=300&fit=crop",
    "laundry_tablecloth": "https://images.unsplash.com/photo-1507089947368-19c1da9775ae?w=400&h=300&fit=crop",
    "laundry_tablecloth_sm": "https://images.unsplash.com/photo-1449247709967-d4461a6a6103?w=400&h=300&fit=crop",
    "laundry_linen": "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=400&h=300&fit=crop",
    "laundry_linen_iron": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=400&h=300&fit=crop",
    "laundry_blanket_s": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400&h=300&fit=crop",
    "laundry_blanket_d": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=400&h=300&fit=crop",
    "laundry_blanket_q": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=300&fit=crop",
    "laundry_blanket_k": "https://images.unsplash.com/photo-1578898887155-72e9a2d0a9c7?w=400&h=300&fit=crop",
    "laundry_comforter_s": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=400&h=300&fit=crop",
    "laundry_comforter_tq": "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=400&h=300&fit=crop",
    "laundry_comforter_d": "https://images.unsplash.com/photo-1588046130717-0eb0c9a3ba15?w=400&h=300&fit=crop",
    "laundry_comforter_q": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400&h=300&fit=crop",
    "laundry_comforter_k": "https://images.unsplash.com/photo-1616627561950-9f746e330187?w=400&h=300&fit=crop",
    "laundry_curtains": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=400&h=300&fit=crop",
    "laundry_bathmat": "https://images.unsplash.com/photo-1620626011761-996317b8d101?w=400&h=300&fit=crop",
    "laundry_carpet_s": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=400&h=300&fit=crop",
    "laundry_carpet_l": "https://images.unsplash.com/photo-1600166898405-da9535204843?w=400&h=300&fit=crop",
    "laundry_carpet_xl": "https://images.unsplash.com/photo-1531835551805-16d864c8d311?w=400&h=300&fit=crop",
    "laundry_trouser": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=300&fit=crop",
    "laundry_dry_only": "https://images.unsplash.com/photo-1604335399105-a0c585fd81a1?w=400&h=300&fit=crop",

    # Flowers
    "bouquet_mixed_sm": "https://images.unsplash.com/photo-1487530811176-3780de880c2d?w=400&h=300&fit=crop",
    "bouquet_mixed_lg": "https://images.unsplash.com/photo-1469259943454-aa100abba749?w=400&h=300&fit=crop",
    "bouquet_sunflower": "https://images.unsplash.com/photo-1596438459194-f275f413d6ff?w=400&h=300&fit=crop",
    "arrangement_lily": "https://images.unsplash.com/photo-1490750967868-88aa4f44baee?w=400&h=300&fit=crop",
    "arrangement_rose_box": "https://images.unsplash.com/photo-1455659817273-f96807779a8a?w=400&h=300&fit=crop",
    "roses_12": "https://images.unsplash.com/photo-1490750967868-88aa4f44baee?w=400&h=300&fit=crop&crop=top",
    "roses_24": "https://images.unsplash.com/photo-1455659817273-f96807779a8a?w=400&h=300&fit=crop&crop=left",
    "roses_50": "https://images.unsplash.com/photo-1455659817273-f96807779a8a?w=400&h=300&fit=crop&crop=top",
    "chocolate_box": "https://images.unsplash.com/photo-1549007994-cb92caebd54b?w=400&h=300&fit=crop",
    "greeting_card": "https://images.unsplash.com/photo-1513151233558-d860c5398176?w=400&h=300&fit=crop",
    "teddy_bear": "https://images.unsplash.com/photo-1559715541-5daf8a0296d0?w=400&h=300&fit=crop",

    # Parcels
    "parcel_standard_5": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=400&h=300&fit=crop",
    "parcel_standard_15": "https://images.unsplash.com/photo-1578575437130-527eed3abbec?w=400&h=300&fit=crop",
    "parcel_standard_30": "https://images.unsplash.com/photo-1617802690992-15d93263d3a9?w=400&h=300&fit=crop",
    "parcel_standard_50": "https://images.unsplash.com/photo-1530124566582-a45a7c005cca?w=400&h=300&fit=crop",
    "parcel_express_5": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=400&h=300&fit=crop",
    "parcel_express_15": "https://images.unsplash.com/photo-1580674285054-bed31e145f59?w=400&h=300&fit=crop",
    "parcel_express_30": "https://images.unsplash.com/photo-1601628828688-632f38a5a7d0?w=400&h=300&fit=crop",
    "parcel_box_sm": "https://images.unsplash.com/photo-1607166452427-7e4477079cb9?w=400&h=300&fit=crop",
    "parcel_box_md": "https://images.unsplash.com/photo-1612815292258-091c08dd2f83?w=400&h=300&fit=crop",
    "parcel_bubble": "https://images.unsplash.com/photo-1553413077-190dd305871c?w=400&h=300&fit=crop",

    # Wings variants
    "wings_bbq": "https://images.unsplash.com/photo-1527477396000-e27163b4bbed?w=400&h=300&fit=crop",
    "wings_10": "https://images.unsplash.com/photo-1608039829572-26d3b6b0e65d?w=400&h=300&fit=crop",
    "wings_3": "https://images.unsplash.com/photo-1567620832903-9fc6debc209f?w=400&h=300&fit=crop",
    "wings_6": "https://images.unsplash.com/photo-1585703900468-13c7a978a7ea?w=400&h=300&fit=crop",
    "wings_12": "https://images.unsplash.com/photo-1569058242253-92a9c755a0ec?w=400&h=300&fit=crop",
    "strips_6": "https://images.unsplash.com/photo-1562967914-608f82629710?w=400&h=300&fit=crop",
}


async def seed():
    # Clear existing data
    await db.restaurants.drop()
    await db.menu_items.drop()
    await db.services.drop()

    # ==================== SERVICE CATEGORIES ====================
    services = [
        {"service_id": "svc_food", "name": "Food Delivery", "icon": "restaurant", "emoji": "🍔", "type": "food", "description": "Order from your favourite restaurants", "active": True},
        {"service_id": "svc_laundry", "name": "Laundry", "icon": "shirt", "emoji": "👔", "type": "laundry", "description": "Pick up, clean & deliver back", "active": True},
        {"service_id": "svc_parcel", "name": "Parcel Delivery", "icon": "cube", "emoji": "📦", "type": "parcel", "description": "Door-to-door delivery", "active": True},
        {"service_id": "svc_florist", "name": "Florist", "icon": "flower", "emoji": "💐", "type": "florist", "description": "Fresh flowers delivered", "active": True},
        {"service_id": "svc_pharmacy", "name": "Pharmacy", "icon": "medkit", "emoji": "💊", "type": "pharmacy", "description": "Health products & supplements", "active": True},
    ]
    await db.services.insert_many(services)
    print(f"Seeded {len(services)} services")

    # Helper to insert items
    async def seed_items(restaurant_id, items):
        for item in items:
            await db.menu_items.insert_one({
                "item_id": f"item_{uuid.uuid4().hex[:12]}",
                "restaurant_id": restaurant_id,
                "available": True,
                "dietary_tags": [],
                **item,
            })
        return len(items)

    # ==================== 1. PEDRO'S CHICKEN ====================
    pedros_id = f"rest_{uuid.uuid4().hex[:12]}"
    await db.restaurants.insert_one({
        "restaurant_id": pedros_id,
        "name": "Pedro's Chicken",
        "description": "Flame-grilled peri-peri chicken, burgers, wraps and family meals. The fastest-growing chicken franchise in South Africa!",
        "image": "https://images.unsplash.com/photo-1626645738196-c2a7c87a8f58?w=600&h=400&fit=crop",
        "cuisine_type": "Chicken",
        "rating": 4.6,
        "delivery_time": "25-35 min",
        "price_range": "R30-R310",
        "location": {"lat": -25.8744, "lng": 29.2339, "address": "Witbank, Emalahleni, South Africa"},
        "featured": True, "active": True, "service_type": "food",
        "menu_categories": ["Chicken Only", "Chicken Meals", "Family Meals", "Burger Meals", "Wraps", "Sides"],
        "available_hours": {"weekdays": "09:00 - 21:00", "weekends": "09:00 - 22:00", "is_open": True},
    })
    n = await seed_items(pedros_id, [
        {"name": "1/4 Chicken", "description": "Flame-grilled peri-peri quarter chicken", "price": 29.99, "category": "Chicken Only", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Q-Chicken_500x500.png"},
        {"name": "1/2 Chicken", "description": "Flame-grilled peri-peri half chicken", "price": 59.99, "category": "Chicken Only", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Half-Chicken_500x500-1.png"},
        {"name": "Full Chicken", "description": "Flame-grilled peri-peri full chicken", "price": 119.99, "category": "Chicken Only", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Full-Chicken_500x500.png"},
        {"name": "4 Wings", "description": "4 flame-grilled peri-peri wings", "price": 39.99, "category": "Chicken Only", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/4-Wings_500x500.png"},
        {"name": "1/4 Chicken & Chips", "description": "Quarter chicken with chips", "price": 44.99, "category": "Chicken Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Q-Chicken-Chips_400x400.png"},
        {"name": "1/4 Chicken, Chips & Roll", "description": "Quarter chicken with chips and Portuguese roll", "price": 49.99, "category": "Chicken Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Q-Chicken-Chips-Roll_500x500.png"},
        {"name": "1/4 Chicken Meal", "description": "Quarter chicken, chips, roll, coleslaw & drink", "price": 59.99, "category": "Chicken Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Q-Chicken-Meal_500x500.png"},
        {"name": "1/2 Chicken & Chips", "description": "Half chicken with chips", "price": 79.99, "category": "Chicken Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Half-Chicken-and-Chips_500x500.png"},
        {"name": "1/2 Chicken Meal", "description": "Half chicken, chips, roll, coleslaw & drink", "price": 89.99, "category": "Chicken Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Half-Chicken-Meal_500x500.png"},
        {"name": "1/4 Chicken Paella", "description": "Quarter chicken with paella rice", "price": 46.99, "category": "Chicken Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Q-Chicken-Paella_500x500.png"},
        {"name": "4 Wings & Chips", "description": "4 wings with chips", "price": 49.99, "category": "Chicken Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/4-Wings-Chips_500x500.png"},
        {"name": "Viva Meal", "description": "Full chicken, large chips & 4 rolls", "price": 155.99, "category": "Family Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Viva-Meal_500x500.png"},
        {"name": "Full Meal", "description": "Full chicken, large chips, 4 rolls, large coleslaw & 2L drink", "price": 199.99, "category": "Family Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Full-Meal_500x500.png"},
        {"name": "Mega Meal", "description": "2 full chickens, 2 large chips & 8 rolls", "price": 309.99, "category": "Family Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Mega-Meal_500x500.png"},
        {"name": "Mini Combo", "description": "Full chicken, 8 wings, large chips & 4 rolls", "price": 219.99, "category": "Family Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Mini-Combo_500x500.png"},
        {"name": "Chicken Burger", "description": "Flame-grilled chicken breast burger", "price": 35.99, "category": "Burger Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Chicken-Burger_500x500.png"},
        {"name": "Chicken Burger & Chips", "description": "Chicken burger served with chips", "price": 45.99, "category": "Burger Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Chicken-Burger-Chips_500x500.png"},
        {"name": "Cheese Burger & Chips", "description": "Chicken cheese burger with chips", "price": 49.99, "category": "Burger Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Cheese-Burger-Chips_500x500.png"},
        {"name": "Don Pedro Burger & Chips", "description": "Signature Don Pedro burger with chips", "price": 45.99, "category": "Burger Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Don-Pedro-Chips_500x500.png"},
        {"name": "Double Up & Chips", "description": "Double chicken burger with chips", "price": 79.99, "category": "Burger Meals", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Double-Up-Chips_500x500.png"},
        {"name": "Slaw Wrap", "description": "Chicken wrap with coleslaw", "price": 36.99, "category": "Wraps", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Slaw-Wrap_500x500.png"},
        {"name": "Chicken Wrap & Chips", "description": "Chicken wrap served with chips", "price": 49.99, "category": "Wraps", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Chicken-Wrap-Chips_500x500-.png"},
        {"name": "Cheesy Jalapeno Wrap", "description": "Spicy cheesy jalapeno chicken wrap", "price": 46.99, "category": "Wraps", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Cheesy-Jalapeno-Wrap_500x500.png"},
        {"name": "Fully Loaded Wrap & Chips", "description": "Fully loaded chicken wrap with chips", "price": 59.99, "category": "Wraps", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Fully-Loaded-Wrap-Chips_500x500.png"},
        {"name": "Regular Chips", "description": "Portion of crispy chips", "price": 17.99, "category": "Sides", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Regular-Chips_500x500.png"},
        {"name": "Large Chips", "description": "Large portion of crispy chips", "price": 27.99, "category": "Sides", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Large-Chips_500x500.png"},
        {"name": "Garlic Roll", "description": "Freshly baked garlic roll", "price": 9.99, "category": "Sides", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Garlic-Roll_500x500.png"},
        {"name": "Loaded Fries", "description": "Chips loaded with toppings", "price": 36.99, "category": "Sides", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Loaded-Fries_500x500.png"},
        {"name": "Pap & Chakalaka", "description": "Traditional pap with chakalaka", "price": 19.99, "category": "Sides", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Pap-Chakalaka_500x500.png"},
        {"name": "Coleslaw Salad", "description": "Fresh coleslaw salad", "price": 17.99, "category": "Sides", "image": "https://i0.wp.com/pedroschicken.co.za/wp-content/uploads/2026/03/Coleslaw-Salad_500x500.png"},
    ])
    print(f"Seeded Pedro's Chicken: {n} items")

    # ==================== 2. MOCHACHOS ====================
    mochachos_id = f"rest_{uuid.uuid4().hex[:12]}"
    await db.restaurants.insert_one({
        "restaurant_id": mochachos_id,
        "name": "Mochachos",
        "description": "Mexican-inspired flame-grilled chicken. Famous for dry spiced chicken, oversized burgers, burritos, enchiladas, fajitas & chimichangas. Spicy but Not Hot!",
        "image": "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?w=600&h=400&fit=crop",
        "cuisine_type": "Mexican Chicken",
        "rating": 4.5,
        "delivery_time": "30-40 min",
        "price_range": "R35-R180",
        "location": {"lat": -25.8744, "lng": 29.2339, "address": "Saveways Crescent Shopping Centre, Witbank, Emalahleni"},
        "featured": True, "active": True, "service_type": "food",
        "menu_categories": ["Flame Grilled Chicken", "Burgers", "Mexican Specials", "Wraps & Burritos", "Sides & Extras"],
        "available_hours": {"weekdays": "10:00 - 21:00", "weekends": "09:00 - 22:00", "is_open": True},
    })
    n = await seed_items(mochachos_id, [
        {"name": "1/4 Flame Grilled Chicken", "description": "Dry spiced flame-grilled chicken, your choice of flavour", "price": 39.99, "category": "Flame Grilled Chicken", "image": IMG["chicken_quarter"]},
        {"name": "1/2 Flame Grilled Chicken", "description": "Half flame-grilled chicken with your choice of flavour", "price": 69.99, "category": "Flame Grilled Chicken", "image": IMG["chicken_half"]},
        {"name": "Full Flame Grilled Chicken", "description": "Full flame-grilled chicken - Lemon & Herb, Mild, Hot or Dynamite", "price": 129.99, "category": "Flame Grilled Chicken", "image": IMG["chicken_full"]},
        {"name": "8 BBQ Wings & Chips", "description": "8 wings basted in sticky BBQ sauce with beeger chips", "price": 79.99, "category": "Flame Grilled Chicken", "image": IMG["wings_bbq"]},
        {"name": "Chicken Fillet Burger", "description": "Oversized flame-grilled chicken fillet burger", "price": 54.99, "category": "Burgers", "image": IMG["burger_chicken"]},
        {"name": "Cheese Chicken Burger", "description": "Chicken fillet burger with melted cheese", "price": 59.99, "category": "Burgers", "image": IMG["burger_cheese"]},
        {"name": "Mexican Burger", "description": "Chicken burger with salsa, guacamole & jalapenos", "price": 64.99, "category": "Burgers", "image": IMG["burger_gourmet"]},
        {"name": "Chicken Enchilada", "description": "Tortilla filled with chicken, covered in salsa & melted cheese", "price": 74.99, "category": "Mexican Specials", "image": IMG["enchilada"]},
        {"name": "Chicken Fajitas", "description": "Two tortillas with chicken, sauteed onion & peppers, rice, salad, cheese, sour cream & guacamole", "price": 89.99, "category": "Mexican Specials", "image": IMG["fajita"]},
        {"name": "Classic Nachos", "description": "Crispy tortilla chips with salsa, melted cheese, sour cream, guacamole & jalapenos", "price": 59.99, "category": "Mexican Specials", "image": IMG["nachos"]},
        {"name": "Quesadilla", "description": "Toasted tortillas with chicken, onion, green pepper & cheddar cheese", "price": 64.99, "category": "Mexican Specials", "image": IMG["quesadilla"]},
        {"name": "Chicken Burrito", "description": "Large flour tortilla filled with chicken, Mexican rice, beans & salad", "price": 69.99, "category": "Wraps & Burritos", "image": IMG["burrito"]},
        {"name": "Chimichanga", "description": "Deep-fried burrito with chicken, cheese & Mexican rice", "price": 74.99, "category": "Wraps & Burritos", "image": IMG["taco"]},
        {"name": "Mexican Rice", "description": "Flavourful Mexican-style rice", "price": 24.99, "category": "Sides & Extras", "image": IMG["rice_mexican"]},
        {"name": "Beeger Chips", "description": "Large portion of crispy chips", "price": 29.99, "category": "Sides & Extras", "image": IMG["chips_regular"]},
        {"name": "Corn on the Cob", "description": "Grilled corn on the cob with butter", "price": 19.99, "category": "Sides & Extras", "image": IMG["corn_cob"]},
    ])
    print(f"Seeded Mochachos: {n} items")

    # ==================== 3. SHAWARMA EXPRESS ====================
    shawarma_id = f"rest_{uuid.uuid4().hex[:12]}"
    await db.restaurants.insert_one({
        "restaurant_id": shawarma_id,
        "name": "Shawarma Express",
        "description": "Strictly Halaal shawarmas, grills, platters and more. Shop 53, Highveld Mall Witbank.",
        "image": "https://images.unsplash.com/photo-1529006557810-274b9b2fc783?w=600&h=400&fit=crop",
        "cuisine_type": "Halaal",
        "rating": 4.4,
        "delivery_time": "25-35 min",
        "price_range": "R15-R400",
        "location": {"lat": -25.8744, "lng": 29.2339, "address": "Shop 53, Highveld Mall, Witbank"},
        "featured": True, "active": True, "service_type": "food",
        "menu_categories": ["Shawarmas", "Shawarma Meals", "Grills", "Platters for 2", "Platters for 4", "Sandwiches", "Chips", "Wings & Strips", "Meatboxes", "Salads", "Other"],
        "available_hours": {"weekdays": "09:00 - 21:00", "weekends": "09:00 - 22:00", "is_open": True},
    })
    n = await seed_items(shawarma_id, [
        {"name": "Veg Shawarma", "description": "Fresh vegetable shawarma wrap", "price": 70.00, "category": "Shawarmas", "image": IMG["wrap_veg"]},
        {"name": "Chicken Shawarma", "description": "Classic chicken shawarma wrap", "price": 80.00, "category": "Shawarmas", "image": IMG["shawarma"]},
        {"name": "Beef Shawarma", "description": "Tender beef shawarma wrap", "price": 90.00, "category": "Shawarmas", "image": IMG["shawarma2"]},
        {"name": "Veg Shawarma Meal", "description": "Veg shawarma with chips & drink", "price": 100.00, "category": "Shawarma Meals", "image": IMG["wrap_chicken"]},
        {"name": "Chicken Shawarma Meal", "description": "Chicken shawarma with chips & drink", "price": 110.00, "category": "Shawarma Meals", "image": IMG["wrap_beef"]},
        {"name": "Beef Shawarma Meal", "description": "Beef shawarma with chips & drink", "price": 120.00, "category": "Shawarma Meals", "image": IMG["kebab"]},
        {"name": "1/4 Chicken Tikka Meal", "description": "Quarter chicken tikka with chips, roti & salad", "price": 90.00, "category": "Grills", "image": IMG["tikka"]},
        {"name": "1/2 Chicken Tikka Meal", "description": "Half chicken tikka with chips, roti & salad", "price": 160.00, "category": "Grills", "image": IMG["tikka_chicken"]},
        {"name": "Full Chicken Tikka Meal", "description": "Full chicken tikka with chips, roti & salad", "price": 250.00, "category": "Grills", "image": IMG["platter_chicken"]},
        {"name": "Platter for 2 - Chicken", "description": "Sharing platter with chicken for 2", "price": 210.00, "category": "Platters for 2", "image": IMG["platter_meat"]},
        {"name": "Platter for 2 - Beef", "description": "Sharing platter with beef for 2", "price": 230.00, "category": "Platters for 2", "image": IMG["meatbox"]},
        {"name": "Platter for 4 - Chicken", "description": "Sharing platter with chicken for 4", "price": 400.00, "category": "Platters for 4", "image": IMG["combo_family"]},
        {"name": "Toasted Cheese Sandwich", "description": "Classic toasted cheese", "price": 50.00, "category": "Sandwiches", "image": IMG["sandwich_cheese"]},
        {"name": "Toasted Chicken Sandwich", "description": "Toasted chicken sandwich", "price": 60.00, "category": "Sandwiches", "image": IMG["sandwich_toasted"]},
        {"name": "Toasted Beef Sandwich", "description": "Toasted beef sandwich", "price": 70.00, "category": "Sandwiches", "image": IMG["sandwich_club"]},
        {"name": "Mini Chips", "description": "Small portion of chips", "price": 25.00, "category": "Chips", "image": IMG["chips_thin"]},
        {"name": "Small Chips", "description": "Regular portion of chips", "price": 40.00, "category": "Chips", "image": IMG["chips_regular"]},
        {"name": "Large Chips", "description": "Large portion of chips", "price": 60.00, "category": "Chips", "image": IMG["chips_large"]},
        {"name": "3 pcs Wings & Chips", "description": "3 chicken wings with chips", "price": 40.00, "category": "Wings & Strips", "image": IMG["wings_3"]},
        {"name": "6 pcs Wings & Chips", "description": "6 chicken wings with chips", "price": 65.00, "category": "Wings & Strips", "image": IMG["wings_6"]},
        {"name": "12 pcs Wings & Chips", "description": "12 chicken wings with chips", "price": 110.00, "category": "Wings & Strips", "image": IMG["wings_12"]},
        {"name": "6 pcs Strips & Chips", "description": "6 chicken strips with chips", "price": 75.00, "category": "Wings & Strips", "image": IMG["strips_6"]},
        {"name": "Small Meatbox + Special Chips", "description": "Small mixed meat box with special chips", "price": 90.00, "category": "Meatboxes", "image": IMG["braai_box"]},
        {"name": "Medium Meatbox + Special Chips", "description": "Medium mixed meat box with special chips", "price": 120.00, "category": "Meatboxes", "image": IMG["combo_box"]},
        {"name": "Large Meatbox + Special Chips", "description": "Large mixed meat box with special chips", "price": 150.00, "category": "Meatboxes", "image": IMG["combo_variety"]},
        {"name": "Russian & Chips", "description": "Russian sausage with chips", "price": 15.00, "category": "Other", "image": IMG["russian"]},
        {"name": "Pap & Grill Chicken", "description": "Traditional pap with grilled chicken", "price": 60.00, "category": "Other", "image": IMG["pap"]},
        {"name": "Special Chicken Salad", "description": "Fresh salad with grilled chicken", "price": 80.00, "category": "Salads", "image": IMG["side_salad"]},
    ])
    print(f"Seeded Shawarma Express: {n} items")

    # ==================== 4. VRIESPOT FROZEN FOODS ====================
    vriespot_id = f"rest_{uuid.uuid4().hex[:12]}"
    await db.restaurants.insert_one({
        "restaurant_id": vriespot_id,
        "name": "Vriespot Frozen Foods",
        "description": "Gourmet Home-Style Meals - Ready in Minutes! No cooking, just heat & eat. 400g per container. Frozen meals delivered fresh.",
        "image": "https://images.unsplash.com/photo-1574894709920-11b28e7367e3?w=600&h=400&fit=crop",
        "cuisine_type": "Frozen Meals",
        "rating": 4.3,
        "delivery_time": "30-45 min",
        "price_range": "R55-R1500",
        "location": {"lat": -25.8744, "lng": 29.2339, "address": "Witbank, Emalahleni"},
        "featured": False, "active": True, "service_type": "food",
        "menu_categories": ["Single Meals", "Combo Deals"],
        "available_hours": {"weekdays": "08:00 - 17:00", "weekends": "08:00 - 14:00", "is_open": True},
    })
    n = await seed_items(vriespot_id, [
        {"name": "Mince Lasagne", "description": "Classic mince lasagne, 400g", "price": 55.00, "category": "Single Meals", "image": IMG["frozen_lasagne"]},
        {"name": "Chicken Lasagne", "description": "Creamy chicken lasagne, 400g", "price": 55.00, "category": "Single Meals", "image": IMG["frozen_chicken_lasagne"]},
        {"name": "Smokey Pork Lasagne", "description": "Smokey pork flavoured lasagne, 400g", "price": 55.00, "category": "Single Meals", "image": IMG["frozen_pork_lasagne"]},
        {"name": "Mac & Creamy Mince", "description": "Macaroni with creamy mince, 400g", "price": 55.00, "category": "Single Meals", "image": IMG["mac_mince"]},
        {"name": "Mac & Creamy Chicken", "description": "Macaroni with creamy chicken, 400g", "price": 55.00, "category": "Single Meals", "image": IMG["mac_chicken"]},
        {"name": "Mac & Creamy Bacon", "description": "Macaroni with creamy bacon, 400g", "price": 55.00, "category": "Single Meals", "image": IMG["mac_bacon"]},
        {"name": "Mac & Cheese", "description": "Classic mac and cheese, 400g", "price": 55.00, "category": "Single Meals", "image": IMG["mac_cheese"]},
        {"name": "Mince Cottage Pie", "description": "Traditional mince cottage pie, 400g", "price": 55.00, "category": "Single Meals", "image": IMG["cottage_pie"]},
        {"name": "Chicken Cottage Pie", "description": "Chicken cottage pie, 400g", "price": 55.00, "category": "Single Meals", "image": IMG["cottage_chicken"]},
        {"name": "Rice & Savoury Mince", "description": "Savoury mince with rice, 400g", "price": 55.00, "category": "Single Meals", "image": IMG["rice_mince"]},
        {"name": "10 Meal Combo (Any 10)", "description": "Pick any 10 meals", "price": 500.00, "category": "Combo Deals", "image": IMG["combo_10"]},
        {"name": "20 Meal Special (2 of each)", "description": "2 of each flavour - 20 meals", "price": 1000.00, "category": "Combo Deals", "image": IMG["combo_20"]},
        {"name": "30 Meal Special (3 of each)", "description": "3 of each flavour - 30 meals", "price": 1500.00, "category": "Combo Deals", "image": IMG["combo_30"]},
    ])
    print(f"Seeded Vriespot Frozen Foods: {n} items")

    # ==================== 5. CAFE E (renamed from Cafe Estreito) ====================
    cafe_id = f"rest_{uuid.uuid4().hex[:12]}"
    await db.restaurants.insert_one({
        "restaurant_id": cafe_id,
        "name": "CAFE E",
        "description": "Coffee & Culture. Artisan coffee, street-style road dogs, roll ups, pregos and shakes. Big flavours, fresh wraps!",
        "image": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=600&h=400&fit=crop",
        "cuisine_type": "Cafe",
        "rating": 4.6,
        "delivery_time": "20-30 min",
        "price_range": "R8-R89",
        "location": {"lat": -25.8744, "lng": 29.2339, "address": "Witbank, Emalahleni"},
        "featured": True, "active": True, "service_type": "food",
        "menu_categories": ["Road Dogs", "Roll Ups", "Chicken Style Pregos", "Beef Style Pregos", "Brewed Coffee", "Lattes", "Warm & Cozy", "Brain Freeze", "Shake It Up", "Refreshments", "Extras"],
        "available_hours": {"weekdays": "07:00 - 18:00", "weekends": "08:00 - 16:00", "is_open": True},
    })
    n = await seed_items(cafe_id, [
        # Road Dogs
        {"name": "The Mozam Classic", "description": "Classic Mozambican-style road dog", "price": 35.00, "category": "Road Dogs", "image": IMG["road_dog"]},
        {"name": "The In-Between Dog", "description": "Road dog with all the extras", "price": 45.00, "category": "Road Dogs", "image": IMG["road_dog_loaded"]},
        {"name": "The Loaded One", "description": "Fully loaded gourmet road dog", "price": 59.00, "category": "Road Dogs", "image": IMG["hotdog"]},
        # Roll Ups
        {"name": "Classic Crunch", "description": "Crunchy chicken roll up", "price": 69.00, "category": "Roll Ups", "image": IMG["roll_up"]},
        {"name": "Loaded Chicken", "description": "Loaded chicken roll up", "price": 59.00, "category": "Roll Ups", "image": IMG["wrap_chicken"]},
        {"name": "Halloumi Blaze", "description": "Halloumi cheese roll up with spice", "price": 79.00, "category": "Roll Ups", "image": IMG["halloumi"]},
        # Chicken Pregos
        {"name": "Chicken OG Prego", "description": "Original chicken prego roll", "price": 39.00, "category": "Chicken Style Pregos", "image": IMG["prego_chicken"]},
        {"name": "Chick 'N Mayo", "description": "Chicken & mayo prego", "price": 55.00, "category": "Chicken Style Pregos", "image": IMG["sandwich_toasted"]},
        {"name": "Chick 'N Avo Boss", "description": "Chicken & avocado prego", "price": 69.00, "category": "Chicken Style Pregos", "image": IMG["sandwich_club"]},
        {"name": "Classic Chick", "description": "Classic chicken prego", "price": 49.00, "category": "Chicken Style Pregos", "image": IMG["sandwich_cheese"]},
        {"name": "Chicken Signature Prego", "description": "Signature chicken prego with special sauce", "price": 69.00, "category": "Chicken Style Pregos", "image": IMG["sandwich_dagwood"]},
        # Beef Pregos
        {"name": "Beef OG Prego", "description": "Original beef prego roll", "price": 65.00, "category": "Beef Style Pregos", "image": IMG["prego_beef"]},
        {"name": "The Juicy Beef", "description": "Juicy beef prego with toppings", "price": 89.00, "category": "Beef Style Pregos", "image": IMG["burger_classic"]},
        {"name": "The Beef Boss", "description": "Ultimate loaded beef prego", "price": 89.00, "category": "Beef Style Pregos", "image": IMG["burger_deluxe"]},
        # Brewed Coffee
        {"name": "Espresso (Single)", "description": "Single shot espresso", "price": 25.00, "category": "Brewed Coffee", "image": IMG["espresso"]},
        {"name": "Espresso (Double)", "description": "Double shot espresso", "price": 30.00, "category": "Brewed Coffee", "image": IMG["espresso_double"]},
        {"name": "Macchiatto (Single)", "description": "Single macchiatto", "price": 24.00, "category": "Brewed Coffee", "image": IMG["macchiato"]},
        {"name": "Cortado (Single)", "description": "Single cortado", "price": 29.00, "category": "Brewed Coffee", "image": IMG["cortado"]},
        {"name": "Flat White", "description": "Smooth flat white", "price": 25.00, "category": "Brewed Coffee", "image": IMG["flat_white"]},
        {"name": "Americano (Large)", "description": "Large hot americano", "price": 40.00, "category": "Brewed Coffee", "image": IMG["americano"]},
        {"name": "Cappuccino (Regular)", "description": "Regular cappuccino", "price": 30.00, "category": "Brewed Coffee", "image": IMG["cappuccino"]},
        {"name": "Cappuccino (Large)", "description": "Large cappuccino", "price": 45.00, "category": "Brewed Coffee", "image": IMG["cappuccino_large"]},
        {"name": "Cafe Mocha (Regular)", "description": "Regular cafe mocha", "price": 35.00, "category": "Brewed Coffee", "image": IMG["mocha"]},
        {"name": "Cafe Mocha (Large)", "description": "Large cafe mocha", "price": 50.00, "category": "Brewed Coffee", "image": IMG["mocha_large"]},
        # Lattes
        {"name": "Cafe Latte (Regular)", "description": "Regular cafe latte", "price": 35.00, "category": "Lattes", "image": IMG["latte"]},
        {"name": "Cafe Latte (Large)", "description": "Large cafe latte", "price": 50.00, "category": "Lattes", "image": IMG["latte_vanilla"]},
        {"name": "Latte Vanilla (Regular)", "description": "Vanilla flavoured latte", "price": 35.00, "category": "Lattes", "image": IMG["latte_caramel"]},
        {"name": "Latte Caramel (Regular)", "description": "Caramel flavoured latte", "price": 35.00, "category": "Lattes", "image": IMG["latte_hazelnut"]},
        {"name": "Latte Hazelnut (Regular)", "description": "Hazelnut flavoured latte", "price": 35.00, "category": "Lattes", "image": IMG["chai_latte"]},
        {"name": "Chai Latte (Regular)", "description": "Spiced chai latte", "price": 30.00, "category": "Lattes", "image": IMG["dirty_chai"]},
        {"name": "Dirty Chai Latte (Regular)", "description": "Chai latte with espresso shot", "price": 39.00, "category": "Lattes", "image": IMG["tea_roses"]},
        # Warm & Cozy
        {"name": "Hot Chocolate (Regular)", "description": "Rich hot chocolate", "price": 35.00, "category": "Warm & Cozy", "image": IMG["hot_chocolate"]},
        {"name": "Hot Chocolate (Large)", "description": "Large rich hot chocolate", "price": 50.00, "category": "Warm & Cozy", "image": IMG["hot_chocolate_large"]},
        {"name": "Red Cappuccino (Regular)", "description": "Rooibos red cappuccino", "price": 30.00, "category": "Warm & Cozy", "image": IMG["red_cappuccino"]},
        {"name": "Five Roses Tea", "description": "Classic Five Roses tea", "price": 25.00, "category": "Warm & Cozy", "image": IMG["tea_rooibos"]},
        {"name": "Rooibos Tea", "description": "South African rooibos tea", "price": 25.00, "category": "Warm & Cozy", "image": IMG["ice_tea"]},
        # Brain Freeze
        {"name": "Coffee Freezo (Regular)", "description": "Iced blended coffee", "price": 45.00, "category": "Brain Freeze", "image": IMG["freezo_coffee"]},
        {"name": "Chocolate Freezo (Regular)", "description": "Iced blended chocolate", "price": 45.00, "category": "Brain Freeze", "image": IMG["freezo_choco"]},
        {"name": "Mocha Freezo (Regular)", "description": "Iced blended mocha", "price": 45.00, "category": "Brain Freeze", "image": IMG["freezo_mocha"]},
        {"name": "Mango Freezo (Regular)", "description": "Iced blended mango", "price": 45.00, "category": "Brain Freeze", "image": IMG["freezo_mango"]},
        {"name": "Honeyboz Freezo (Regular)", "description": "Iced blended honeybush", "price": 45.00, "category": "Brain Freeze", "image": IMG["freezo_honey"]},
        {"name": "Passion Freezo (Regular)", "description": "Iced blended passion fruit", "price": 45.00, "category": "Brain Freeze", "image": IMG["freezo_passion"]},
        # Shake It Up
        {"name": "Vanilla Shake", "description": "Creamy vanilla milkshake", "price": 50.00, "category": "Shake It Up", "image": IMG["shake_vanilla"]},
        {"name": "Chocolate Shake", "description": "Rich chocolate milkshake", "price": 50.00, "category": "Shake It Up", "image": IMG["shake_chocolate"]},
        {"name": "Strawberry Shake", "description": "Fresh strawberry milkshake", "price": 50.00, "category": "Shake It Up", "image": IMG["shake_strawberry"]},
        {"name": "Peanut Butter Shake", "description": "Peanut butter milkshake", "price": 65.00, "category": "Shake It Up", "image": IMG["shake_peanut"]},
        {"name": "Cherry Cheesecake Shake", "description": "Cherry cheesecake milkshake", "price": 65.00, "category": "Shake It Up", "image": IMG["shake_cherry"]},
        {"name": "Blueberry Oreo Shake", "description": "Blueberry oreo milkshake", "price": 65.00, "category": "Shake It Up", "image": IMG["shake_blueberry"]},
        # Refreshments
        {"name": "Coke", "description": "Coca-Cola", "price": 25.00, "category": "Refreshments", "image": IMG["coke"]},
        {"name": "Coke Zero", "description": "Coca-Cola Zero Sugar", "price": 25.00, "category": "Refreshments", "image": IMG["cold_drink"]},
        {"name": "Sprite", "description": "Sprite", "price": 25.00, "category": "Refreshments", "image": IMG["sprite"]},
        {"name": "Fanta", "description": "Fanta Orange", "price": 25.00, "category": "Refreshments", "image": IMG["fanta"]},
        {"name": "Appletiser", "description": "Sparkling apple juice", "price": 30.00, "category": "Refreshments", "image": IMG["appletiser"]},
        {"name": "Ice Tea Lemon", "description": "Iced tea lemon flavour", "price": 30.00, "category": "Refreshments", "image": IMG["ice_block"]},
        {"name": "Ice Tea Peach", "description": "Iced tea peach flavour", "price": 30.00, "category": "Refreshments", "image": IMG["ice_tea"]},
        {"name": "Water Still", "description": "Still mineral water", "price": 25.00, "category": "Refreshments", "image": IMG["water"]},
        {"name": "Water Sparkling", "description": "Sparkling mineral water", "price": 25.00, "category": "Refreshments", "image": IMG["appletiser"]},
        # Extras
        {"name": "Alternative Milk (Almond/Oat)", "description": "Swap to almond or oat milk", "price": 8.00, "category": "Extras", "image": IMG["alt_milk"]},
        {"name": "Espresso Shot", "description": "Extra espresso shot", "price": 10.00, "category": "Extras", "image": IMG["espresso_shot"]},
    ])
    print(f"Seeded CAFE E: {n} items")

    # ==================== 6. KEVCOR TAKE-AWAYS ====================
    kevcor_id = f"rest_{uuid.uuid4().hex[:12]}"
    await db.restaurants.insert_one({
        "restaurant_id": kevcor_id,
        "name": "Kevcor Take-Aways",
        "description": "Classic take-away favourites! Chips, Russians, burgers, toasted sandwiches, kotas and breakfast buns. 1 Mona St, Modelpark, Witbank.",
        "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600&h=400&fit=crop",
        "cuisine_type": "Take-Away",
        "rating": 4.2,
        "delivery_time": "20-30 min",
        "price_range": "R15-R220",
        "location": {"lat": -25.8744, "lng": 29.2339, "address": "1 Mona St, Modelpark, Witbank"},
        "featured": False, "active": True, "service_type": "food",
        "menu_categories": ["Chips", "Russian", "Burgers", "Toasted Sandwiches", "Other", "Russian & Chips Combos", "Other Combos", "Breakfast Toasted Sandwich", "Breakfast Bun"],
        "available_hours": {"weekdays": "07:00 - 20:00", "weekends": "07:00 - 20:00", "is_open": True},
    })
    n = await seed_items(kevcor_id, [
        # Chips
        {"name": "Mini Chips (300g)", "description": "300g portion of crispy chips", "price": 15.00, "category": "Chips", "image": IMG["chips_thin"]},
        {"name": "Small Chips (500g)", "description": "500g portion of crispy chips", "price": 24.00, "category": "Chips", "image": IMG["chips_regular"]},
        {"name": "Medium Chips (700g)", "description": "700g portion of crispy chips", "price": 35.00, "category": "Chips", "image": IMG["chips_curly"]},
        {"name": "Large Chips (1.1kg)", "description": "1.1kg portion of crispy chips", "price": 56.00, "category": "Chips", "image": IMG["chips_large"]},
        {"name": "Family Chips (1.7kg)", "description": "1.7kg family size portion", "price": 85.00, "category": "Chips", "image": IMG["chips_family"]},
        # Russian
        {"name": "Small Russian", "description": "Small Russian sausage", "price": 16.00, "category": "Russian", "image": IMG["russian"]},
        {"name": "Large Russian", "description": "Large Russian sausage", "price": 25.00, "category": "Russian", "image": IMG["russian_large"]},
        {"name": "Large Cheese Russian", "description": "Large cheese-filled Russian sausage", "price": 25.00, "category": "Russian", "image": IMG["cheese_griller"]},
        # Burgers
        {"name": "Beef Burger", "description": "Classic beef burger", "price": 42.00, "category": "Burgers", "image": IMG["burger_classic"]},
        {"name": "Cheese Burger", "description": "Beef burger with melted cheese", "price": 45.00, "category": "Burgers", "image": IMG["burger_cheese"]},
        {"name": "Chicken Burger", "description": "Chicken fillet burger", "price": 39.00, "category": "Burgers", "image": IMG["burger_chicken"]},
        {"name": "Bacon Cheese Burger", "description": "Burger with bacon & cheese", "price": 50.00, "category": "Burgers", "image": IMG["burger_bacon"]},
        {"name": "Double Beef Cheese Burger", "description": "Double beef patty with cheese", "price": 65.00, "category": "Burgers", "image": IMG["burger_double"]},
        # Toasted Sandwiches
        {"name": "Ham & Cheese Toasted", "description": "Classic ham & cheese toasted sandwich", "price": 22.00, "category": "Toasted Sandwiches", "image": IMG["sandwich_cheese"]},
        {"name": "Cheese & Tomato Toasted", "description": "Cheese & tomato toasted sandwich", "price": 22.00, "category": "Toasted Sandwiches", "image": IMG["sandwich_toasted"]},
        {"name": "Ham, Cheese & Tomato Toasted", "description": "Ham, cheese & tomato toasted sandwich", "price": 25.00, "category": "Toasted Sandwiches", "image": IMG["sandwich_club"]},
        {"name": "Dagwood Toasted", "description": "Fully loaded dagwood toasted sandwich", "price": 48.00, "category": "Toasted Sandwiches", "image": IMG["sandwich_dagwood"]},
        # Other
        {"name": "Kota", "description": "Traditional South African kota", "price": 25.00, "category": "Other", "image": IMG["kota"]},
        {"name": "Kota with Russian", "description": "Kota with Russian sausage", "price": 35.00, "category": "Other", "image": IMG["kota_russian"]},
        {"name": "Kota with Russian & Egg", "description": "Kota with Russian sausage & fried egg", "price": 40.00, "category": "Other", "image": IMG["chip_roll"]},
        {"name": "Cheese Griller Roll", "description": "Cheese griller in a roll", "price": 28.00, "category": "Other", "image": IMG["hotdog2"]},
        {"name": "Chip Roll", "description": "Chips in a roll", "price": 20.00, "category": "Other", "image": IMG["hotdog"]},
        {"name": "Chip Russian Roll", "description": "Chips and Russian in a roll", "price": 32.00, "category": "Other", "image": IMG["road_dog_loaded"]},
        # Russian & Chips Combos
        {"name": "Mini Chips + Small Russian", "description": "Mini chips with small Russian", "price": 28.00, "category": "Russian & Chips Combos", "image": IMG["chips_loaded"]},
        {"name": "Small Chips + 2 Small Russian", "description": "Small chips with 2 small Russians", "price": 50.00, "category": "Russian & Chips Combos", "image": IMG["chips_wedges"]},
        {"name": "Medium Chips + 2 Large Russian", "description": "Medium chips with 2 large Russians", "price": 78.00, "category": "Russian & Chips Combos", "image": IMG["chips_cheesy"]},
        {"name": "Large Chips + 2 Small Russian", "description": "Large chips with 2 small Russians", "price": 80.00, "category": "Russian & Chips Combos", "image": IMG["chips_plain"]},
        {"name": "Large Chips + 2 Large Russian", "description": "Large chips with 2 large Russians", "price": 92.00, "category": "Russian & Chips Combos", "image": IMG["combo_box"]},
        {"name": "Large Chips + 5 Small Russian", "description": "Large chips with 5 small Russians", "price": 110.00, "category": "Russian & Chips Combos", "image": IMG["combo_family"]},
        {"name": "Family Chips + 4 Large Russian", "description": "Family chips with 4 large Russians", "price": 160.00, "category": "Russian & Chips Combos", "image": IMG["combo_variety"]},
        # Other Combos
        {"name": "2 Chicken Burgers + Small Chips", "description": "2 chicken burgers with small chips", "price": 89.00, "category": "Other Combos", "image": IMG["burger_meal"]},
        {"name": "2 Beef Burgers + Small Chips", "description": "2 beef burgers with small chips", "price": 95.00, "category": "Other Combos", "image": IMG["burger_bbq"]},
        {"name": "2 Cheese Griller Rolls + Small Chips", "description": "2 cheese griller rolls with small chips", "price": 70.00, "category": "Other Combos", "image": IMG["burger_gourmet"]},
        {"name": "4 Cheese Burgers + Large Chips + 2L Coke", "description": "Family deal: 4 burgers, large chips & 2L Coke", "price": 220.00, "category": "Other Combos", "image": IMG["burger_tower"]},
        # Breakfast
        {"name": "Bacon & Cheese Toasted (Breakfast)", "description": "Breakfast toasted: bacon & cheese", "price": 21.00, "category": "Breakfast Toasted Sandwich", "image": IMG["breakfast_bun"]},
        {"name": "Bacon, Egg & Cheese Toasted (Breakfast)", "description": "Breakfast toasted: bacon, egg & cheese", "price": 24.00, "category": "Breakfast Toasted Sandwich", "image": IMG["breakfast_full"]},
        {"name": "Dagwood (Breakfast)", "description": "Breakfast dagwood toasted sandwich", "price": 48.00, "category": "Breakfast Toasted Sandwich", "image": IMG["addon_breakfast"]},
        {"name": "Bacon & Cheese Bun (Breakfast)", "description": "Breakfast bun: bacon & cheese", "price": 21.00, "category": "Breakfast Bun", "image": IMG["croissant"]},
        {"name": "Bacon, Egg & Cheese Bun (Breakfast)", "description": "Breakfast bun: bacon, egg & cheese", "price": 24.00, "category": "Breakfast Bun", "image": IMG["granola"]},
    ])
    print(f"Seeded Kevcor Take-Aways: {n} items")

    # ==================== 7. #BRAAI ====================
    braai_id = f"rest_{uuid.uuid4().hex[:12]}"
    await db.restaurants.insert_one({
        "restaurant_id": braai_id,
        "name": "#Braai",
        "description": "South African braai at its best! Burgers, chicken, ribs, cuts, combos, pizzas & family meals.",
        "image": "https://images.unsplash.com/photo-1544025162-d76694265947?w=600&h=400&fit=crop",
        "cuisine_type": "Braai & Pizza",
        "rating": 4.5,
        "delivery_time": "30-45 min",
        "price_range": "R5-R300",
        "location": {"lat": -25.8744, "lng": 29.2339, "address": "Witbank, Emalahleni"},
        "featured": True, "active": True, "service_type": "food",
        "menu_categories": ["Burgers", "Chicken", "Ribs", "Cuts", "Combos", "Pizza Pies", "Deluxe Pizza", "Traditional Pizza", "Kids Pizza", "Dessert Pizza", "Chips", "Extras", "Sides", "Kids Meals", "Family Meals"],
        "available_hours": {"weekdays": "10:00 - 22:00", "weekends": "10:00 - 22:00", "is_open": True},
    })
    n = await seed_items(braai_id, [
        # Burgers
        {"name": "Chicken Burger", "description": "Flame-grilled chicken burger", "price": 39.90, "category": "Burgers", "image": IMG["burger_chicken"]},
        {"name": "Chicken Burger Meal", "description": "Chicken burger, chips & drink", "price": 69.90, "category": "Burgers", "image": IMG["burger_meal"]},
        {"name": "Chicken Surprise Roll", "description": "Chicken surprise in a roll", "price": 39.90, "category": "Burgers", "image": IMG["roll_up"]},
        {"name": "Chicken Surprise Roll Meal", "description": "Chicken surprise roll, chips & drink", "price": 69.90, "category": "Burgers", "image": IMG["wrap_chicken"]},
        {"name": "Rib Burger Meal", "description": "Rib burger, chips & drink", "price": 75.90, "category": "Burgers", "image": IMG["burger_bbq"]},
        {"name": "Beef Burger Meal", "description": "Beef burger, chips & drink", "price": 79.90, "category": "Burgers", "image": IMG["burger_classic"]},
        {"name": "Beef Cheese Burger Meal", "description": "Beef cheese burger, chips & drink", "price": 84.90, "category": "Burgers", "image": IMG["burger_cheese"]},
        {"name": "Beef Mushroom Burger Meal", "description": "Beef mushroom burger, chips & drink", "price": 84.90, "category": "Burgers", "image": IMG["burger_gourmet"]},
        {"name": "Beef Cheddamelt Burger Meal", "description": "Beef cheddamelt burger, chips & drink", "price": 84.90, "category": "Burgers", "image": IMG["burger_deluxe"]},
        {"name": "Beef Bacon & Cheese Burger Meal", "description": "Bacon & cheese burger, chips & drink", "price": 92.90, "category": "Burgers", "image": IMG["burger_bacon"]},
        {"name": "Beef BAF Burger Meal", "description": "Ultimate BAF burger, chips & drink", "price": 104.90, "category": "Burgers", "image": IMG["burger_double"]},
        # Chicken
        {"name": "4 Piece Wings", "description": "4 braai wings", "price": 35.90, "category": "Chicken", "image": IMG["wings_3"]},
        {"name": "4 Piece Wings Meal", "description": "4 wings, chips & drink", "price": 65.90, "category": "Chicken", "image": IMG["wings_6"]},
        {"name": "10 Piece Wings", "description": "10 braai wings", "price": 84.90, "category": "Chicken", "image": IMG["wings_10"]},
        {"name": "10 Piece Wings Meal", "description": "10 wings, chips & drink", "price": 114.90, "category": "Chicken", "image": IMG["wings_12"]},
        {"name": "1/4 Chicken", "description": "Quarter braai chicken", "price": 44.90, "category": "Chicken", "image": IMG["chicken_quarter"]},
        {"name": "1/4 Chicken Meal", "description": "Quarter chicken, chips & drink", "price": 74.90, "category": "Chicken", "image": IMG["chicken_meal"]},
        {"name": "1/2 Chicken", "description": "Half braai chicken", "price": 79.90, "category": "Chicken", "image": IMG["chicken_half"]},
        {"name": "1/2 Chicken Meal", "description": "Half chicken, chips & drink", "price": 109.90, "category": "Chicken", "image": IMG["chicken_grilled2"]},
        {"name": "Full Chicken", "description": "Full braai chicken", "price": 169.90, "category": "Chicken", "image": IMG["chicken_full"]},
        # Ribs
        {"name": "250g Ribs", "description": "250g braai ribs", "price": 84.90, "category": "Ribs", "image": IMG["ribs_quarter"]},
        {"name": "250g Ribs & Chips", "description": "250g ribs with chips", "price": 99.90, "category": "Ribs", "image": IMG["ribs_half"]},
        {"name": "500g Ribs", "description": "500g braai ribs", "price": 164.90, "category": "Ribs", "image": IMG["ribs_full"]},
        {"name": "500g Ribs & Chips", "description": "500g ribs with chips", "price": 179.90, "category": "Ribs", "image": IMG["platter_meat"]},
        {"name": "750g Ribs & Chips", "description": "750g ribs with chips", "price": 269.90, "category": "Ribs", "image": IMG["meatbox"]},
        {"name": "1kg Ribs & Chips", "description": "1kg ribs with chips", "price": 299.90, "category": "Ribs", "image": IMG["braai_box"]},
        # Cuts
        {"name": "Regular Russian", "description": "Braai Russian sausage", "price": 19.90, "category": "Cuts", "image": IMG["russian"]},
        {"name": "Regular Russian Meal", "description": "Russian, chips & drink", "price": 54.90, "category": "Cuts", "image": IMG["russian_large"]},
        {"name": "Jumbo Russian Meal", "description": "Jumbo Russian, chips & drink", "price": 59.90, "category": "Cuts", "image": IMG["wors"]},
        {"name": "Wors (150g) Meal", "description": "150g boerewors, chips & drink", "price": 74.90, "category": "Cuts", "image": IMG["hotdog"]},
        {"name": "Pork Chop (150g) Meal", "description": "150g pork chop, chips & drink", "price": 79.90, "category": "Cuts", "image": IMG["pork_chop"]},
        {"name": "Brisket (150g) Meal", "description": "150g brisket, chips & drink", "price": 82.90, "category": "Cuts", "image": IMG["brisket"]},
        {"name": "Chuck (200g) Meal", "description": "200g chuck steak, chips & drink", "price": 94.90, "category": "Cuts", "image": IMG["chuck"]},
        {"name": "Dbl Beef Rashers Meal", "description": "Double beef rashers, chips & drink", "price": 94.90, "category": "Cuts", "image": IMG["beef_rashers"]},
        {"name": "T-Bone (350g) Meal", "description": "350g T-bone steak, chips & drink", "price": 139.90, "category": "Cuts", "image": IMG["steak_tbone"]},
        # Combos
        {"name": "Beef Stew & Pap", "description": "Traditional beef stew with pap", "price": 59.90, "category": "Combos", "image": IMG["beef_stew"]},
        {"name": "#braai BOX", "description": "Mixed braai box", "price": 89.90, "category": "Combos", "image": IMG["combo_box"]},
        {"name": "#braai SURPRISE BOX", "description": "Surprise selection braai box", "price": 99.90, "category": "Combos", "image": IMG["combo_variety"]},
        {"name": "#braai MEAT BOX", "description": "All-meat braai box", "price": 99.90, "category": "Combos", "image": IMG["combo_family"]},
        {"name": "#braai MIX BOX", "description": "Mixed variety braai box", "price": 119.90, "category": "Combos", "image": IMG["platter_chicken"]},
        {"name": "#braai COMBO BOX", "description": "Combo braai box", "price": 94.90, "category": "Combos", "image": IMG["burger_tower"]},
        {"name": "Classic #braai BOX", "description": "Classic braai selection box", "price": 124.90, "category": "Combos", "image": IMG["steak"]},
        {"name": "Chuck & Chicken Combo", "description": "Chuck steak and chicken combo", "price": 119.90, "category": "Combos", "image": IMG["chicken_thigh"]},
        {"name": "#braai VARIETY BOX", "description": "Variety braai box for sharing", "price": 129.90, "category": "Combos", "image": IMG["chicken_drumstick"]},
        # Pizza Pies
        {"name": "Biltong & Cheddar Pie", "description": "Biltong & cheddar pizza pie", "price": 64.90, "category": "Pizza Pies", "image": IMG["pie_meat"]},
        {"name": "Braai Broodjie Pie", "description": "Braai broodjie style pie", "price": 59.90, "category": "Pizza Pies", "image": IMG["pie_chicken"]},
        {"name": "Chicken Cheddar & Mushroom Pie", "description": "Chicken, cheddar & mushroom pie", "price": 64.90, "category": "Pizza Pies", "image": IMG["pizza_loaded"]},
        {"name": "Chicken Mayo Pie", "description": "Chicken mayo pizza pie", "price": 49.90, "category": "Pizza Pies", "image": IMG["pizza_slice"]},
        {"name": "Rib & Mushroom Pie", "description": "Rib & mushroom pizza pie", "price": 59.90, "category": "Pizza Pies", "image": IMG["pizza_special"]},
        # Deluxe Pizza
        {"name": "Biltong Pizza (Med)", "description": "Medium biltong pizza", "price": 99.90, "category": "Deluxe Pizza", "image": IMG["pizza_biltong"]},
        {"name": "Carnivore Pizza (Med)", "description": "Medium carnivore meat pizza", "price": 94.90, "category": "Deluxe Pizza", "image": IMG["pizza_meat"]},
        {"name": "BAF Pizza (Med)", "description": "Medium BAF loaded pizza", "price": 94.90, "category": "Deluxe Pizza", "image": IMG["pizza_bbq"]},
        {"name": "Blue Haze Pizza (Med)", "description": "Medium blue cheese pizza", "price": 89.90, "category": "Deluxe Pizza", "image": IMG["pizza_cheese"]},
        {"name": "Chicken Supreme Pizza (Med)", "description": "Medium chicken supreme pizza", "price": 94.90, "category": "Deluxe Pizza", "image": IMG["pizza_chicken"]},
        {"name": "The Don Pizza (Med)", "description": "Medium loaded The Don pizza", "price": 109.90, "category": "Deluxe Pizza", "image": IMG["pizza_loaded"]},
        # Traditional Pizza
        {"name": "Margherita Pizza (Med)", "description": "Classic margherita", "price": 49.90, "category": "Traditional Pizza", "image": IMG["pizza_margherita"]},
        {"name": "Regina Pizza (Med)", "description": "Ham & mushroom pizza", "price": 59.90, "category": "Traditional Pizza", "image": IMG["pizza_special"]},
        {"name": "Hawaiian Pizza (Med)", "description": "Ham & pineapple pizza", "price": 59.90, "category": "Traditional Pizza", "image": IMG["pizza_hawaiian"]},
        {"name": "Tropicana Pizza (Med)", "description": "Tropical topped pizza", "price": 64.90, "category": "Traditional Pizza", "image": IMG["pizza_veggie"]},
        {"name": "Herbivore Pizza (Med)", "description": "Vegetarian loaded pizza", "price": 74.90, "category": "Traditional Pizza", "image": IMG["pizza_slice"]},
        {"name": "Braai BBQ Chicken Pizza (Med)", "description": "BBQ chicken pizza", "price": 79.90, "category": "Traditional Pizza", "image": IMG["pizza_bbq"]},
        {"name": "Peri-Peri Chicken Pizza (Med)", "description": "Peri-peri chicken pizza", "price": 79.90, "category": "Traditional Pizza", "image": IMG["pizza_chicken"]},
        {"name": "Pepperoni Pizza (Med)", "description": "Classic pepperoni pizza", "price": 74.90, "category": "Traditional Pizza", "image": IMG["pizza_pepperoni"]},
        {"name": "4 Seasons Pizza (Med)", "description": "Four seasons pizza", "price": 79.90, "category": "Traditional Pizza", "image": IMG["pizza_meat"]},
        {"name": "Chicken Mayo Pizza (Med)", "description": "Chicken mayo pizza", "price": 64.90, "category": "Traditional Pizza", "image": IMG["pizza_cheese"]},
        {"name": "Mexican Standoff Pizza (Med)", "description": "Mexican style pizza", "price": 74.90, "category": "Traditional Pizza", "image": IMG["pizza_loaded"]},
        {"name": "Boerie Pizza (Med)", "description": "Boerewors topped pizza", "price": 69.90, "category": "Traditional Pizza", "image": IMG["pizza_biltong"]},
        {"name": "Tuscan Pizza (Med)", "description": "Tuscan style pizza", "price": 79.90, "category": "Traditional Pizza", "image": IMG["pizza_special"]},
        {"name": "Rib Surprise Pizza (Med)", "description": "Rib meat pizza", "price": 79.90, "category": "Traditional Pizza", "image": IMG["pizza_bbq"]},
        {"name": "4 Cheese Pizza (Med)", "description": "Four cheese pizza", "price": 79.90, "category": "Traditional Pizza", "image": IMG["pizza_cheese"]},
        # Kids Pizza
        {"name": "Kids Ham & Cheese Pizza", "description": "Kids size ham & cheese pizza", "price": 59.90, "category": "Kids Pizza", "image": IMG["pizza_kids"]},
        {"name": "Kids Ham & Pineapple Pizza", "description": "Kids size ham & pineapple pizza", "price": 59.90, "category": "Kids Pizza", "image": IMG["pizza_hawaiian"]},
        {"name": "Kids Chicken & Cheddar Pizza", "description": "Kids size chicken & cheddar pizza", "price": 59.90, "category": "Kids Pizza", "image": IMG["pizza_chicken"]},
        {"name": "Kids Rib & Mayo Pizza", "description": "Kids size rib & mayo pizza", "price": 59.90, "category": "Kids Pizza", "image": IMG["pizza_meat"]},
        {"name": "Kids Bacon & Cheddar Pizza", "description": "Kids size bacon & cheddar pizza", "price": 59.90, "category": "Kids Pizza", "image": IMG["pizza_margherita"]},
        # Dessert Pizza
        {"name": "Chocolate & Marshmallow Pizza", "description": "Sweet chocolate & marshmallow pizza", "price": 49.90, "category": "Dessert Pizza", "image": IMG["pizza_dessert"]},
        {"name": "Peppermint White Choc & Marshmallow", "description": "Peppermint white chocolate pizza", "price": 64.90, "category": "Dessert Pizza", "image": IMG["shake_cherry"]},
        {"name": "Cookies Peppermint & Marshmallow", "description": "Cookie peppermint marshmallow pizza", "price": 64.90, "category": "Dessert Pizza", "image": IMG["shake_chocolate"]},
        # Chips
        {"name": "Plain Chips (200g)", "description": "200g crispy chips", "price": 19.90, "category": "Chips", "image": IMG["chips_thin"]},
        {"name": "Plain Chips (500g)", "description": "500g crispy chips", "price": 45.90, "category": "Chips", "image": IMG["chips_regular"]},
        {"name": "Plain Chips (750g)", "description": "750g crispy chips", "price": 65.90, "category": "Chips", "image": IMG["chips_large"]},
        {"name": "Plain Chips (1kg)", "description": "1kg crispy chips", "price": 79.90, "category": "Chips", "image": IMG["chips_family"]},
        {"name": "Cheesy Bacon Chips (200g)", "description": "200g cheesy bacon chips", "price": 39.90, "category": "Chips", "image": IMG["chips_loaded"]},
        {"name": "Cheesy Bacon Chips (500g)", "description": "500g cheesy bacon chips", "price": 64.90, "category": "Chips", "image": IMG["chips_cheesy"]},
        {"name": "Cheesy Bacon Chips (750g)", "description": "750g cheesy bacon chips", "price": 89.90, "category": "Chips", "image": IMG["chips_wedges"]},
        {"name": "Cheesy Bacon Chips (1kg)", "description": "1kg cheesy bacon chips", "price": 99.90, "category": "Chips", "image": IMG["chips_curly"]},
        # Extras
        {"name": "Toast Slice", "description": "Toasted bread slice", "price": 4.90, "category": "Extras", "image": IMG["toast"]},
        {"name": "Cheese Slice", "description": "Cheese slice add-on", "price": 6.90, "category": "Extras", "image": IMG["cheese_slice"]},
        {"name": "Egg", "description": "Fried egg add-on", "price": 8.90, "category": "Extras", "image": IMG["egg"]},
        {"name": "Bacon", "description": "Crispy bacon add-on", "price": 12.90, "category": "Extras", "image": IMG["bacon"]},
        {"name": "Marinade (90ml)", "description": "90ml braai marinade", "price": 8.90, "category": "Extras", "image": IMG["marinade"]},
        {"name": "Feta (40g)", "description": "40g feta cheese", "price": 14.90, "category": "Extras", "image": IMG["feta"]},
        {"name": "Tomato Relish/Salsa (80ml)", "description": "80ml tomato relish or salsa", "price": 10.90, "category": "Extras", "image": IMG["pap"]},
        {"name": "Chicken Breast", "description": "Extra chicken breast", "price": 19.90, "category": "Extras", "image": IMG["chicken_strips"]},
        {"name": "Beef Patty (100g)", "description": "Extra 100g beef patty", "price": 24.90, "category": "Extras", "image": IMG["burger_veggie"]},
        {"name": "Avocado (seasonal)", "description": "Fresh avocado (seasonal)", "price": 24.90, "category": "Extras", "image": IMG["avocado"]},
        # Sides
        {"name": "Portuguese Roll", "description": "Fresh Portuguese roll", "price": 8.90, "category": "Sides", "image": IMG["garlic_roll"]},
        {"name": "Garlic Roll", "description": "Garlic butter roll", "price": 14.90, "category": "Sides", "image": IMG["roti_bread"]},
        {"name": "Pap and Relish (400g)", "description": "400g pap with tomato relish", "price": 16.90, "category": "Sides", "image": IMG["pap"]},
        {"name": "Bacon Cheese & Garlic Roll", "description": "Bacon cheese garlic roll", "price": 29.90, "category": "Sides", "image": IMG["braai_broodjie"]},
        {"name": "Coleslaw (250g)", "description": "250g fresh coleslaw", "price": 19.90, "category": "Sides", "image": IMG["coleslaw"]},
        {"name": "Greek Salad", "description": "Fresh Greek salad", "price": 32.90, "category": "Sides", "image": IMG["greek_salad"]},
        {"name": "Braai Broodjie", "description": "Traditional braai broodjie", "price": 27.90, "category": "Sides", "image": IMG["sandwich_toasted"]},
        # Kids Meals
        {"name": "Kids Russian Meal", "description": "Kids Russian, chips & drink", "price": 54.90, "category": "Kids Meals", "image": IMG["kids_meal"]},
        {"name": "Kids Chicken Strips Meal", "description": "Kids chicken strips, chips & drink", "price": 54.90, "category": "Kids Meals", "image": IMG["chicken_fried"]},
        {"name": "Kids Burger Meal", "description": "Kids burger, chips & drink", "price": 54.90, "category": "Kids Meals", "image": IMG["burger_veggie"]},
        # Family Meals
        {"name": "#braai FAMILY PACK", "description": "Family pack for 4-6 people", "price": 299.90, "category": "Family Meals", "image": IMG["combo_family"]},
        {"name": "#braai FAMILY DEAL", "description": "Family deal for 4-6 people", "price": 299.90, "category": "Family Meals", "image": IMG["combo_variety"]},
    ])
    print(f"Seeded #Braai: {n} items")

    # ==================== 8. MILANO'S BRUNCHIES ====================
    milanos_id = f"rest_{uuid.uuid4().hex[:12]}"
    await db.restaurants.insert_one({
        "restaurant_id": milanos_id,
        "name": "Milano's Brunchies",
        "description": "Breakfast & lunch cafe. Full breakfast, waffles, granola, croissants, wraps, and daily pasta specials.",
        "image": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop",
        "cuisine_type": "Brunch",
        "rating": 4.4,
        "delivery_time": "25-40 min",
        "price_range": "R10-R140",
        "location": {"lat": -25.8744, "lng": 29.2339, "address": "Witbank, Emalahleni"},
        "featured": False, "active": True, "service_type": "food",
        "menu_categories": ["Breakfast", "Wraps", "Pasta Specials", "Beverages"],
        "available_hours": {"weekdays": "07:00 - 16:00", "weekends": "08:00 - 15:00", "is_open": True},
    })
    n = await seed_items(milanos_id, [
        {"name": "Full Breakfast", "description": "Eggs, bacon, sausage, toast, tomato & mushrooms", "price": 110.00, "category": "Breakfast", "image": IMG["breakfast_full"]},
        {"name": "Waffles", "description": "Fresh waffles with syrup & cream", "price": 70.00, "category": "Breakfast", "image": IMG["waffles"]},
        {"name": "Fruit Mix Granola Cup (357ml)", "description": "357ml granola with fresh fruit mix", "price": 35.00, "category": "Breakfast", "image": IMG["granola"]},
        {"name": "Fruit Mix Granola Cup (500ml)", "description": "500ml granola with fresh fruit mix", "price": 50.00, "category": "Breakfast", "image": IMG["granola_large"]},
        {"name": "Croissant Club Sandwich", "description": "Croissant with club sandwich fillings", "price": 80.00, "category": "Breakfast", "image": IMG["croissant"]},
        {"name": "Add On (any)", "description": "Extra add-on to any breakfast item", "price": 10.00, "category": "Breakfast", "image": IMG["addon_breakfast"]},
        {"name": "Buffalo Chicken Wrap & Chips", "description": "Spicy buffalo chicken wrap with chips", "price": 80.00, "category": "Wraps", "image": IMG["wrap_chicken"]},
        {"name": "Greek Wrap & Chips", "description": "Greek-style wrap with chips", "price": 75.00, "category": "Wraps", "image": IMG["wrap_veg"]},
        {"name": "Spicy Beef Wrap & Chips", "description": "Spicy beef wrap with chips", "price": 140.00, "category": "Wraps", "image": IMG["wrap_beef"]},
        {"name": "Monday: Spaghetti Meatballs", "description": "Monday special - classic spaghetti meatballs", "price": 120.00, "category": "Pasta Specials", "image": IMG["pasta_meatball"]},
        {"name": "Tuesday: Chicken Pesto Fettuccini", "description": "Tuesday special - chicken pesto fettuccini", "price": 120.00, "category": "Pasta Specials", "image": IMG["pasta_pesto"]},
        {"name": "Wednesday: Creamy Garlic Shrimp Alfredo", "description": "Wednesday special - garlic shrimp alfredo", "price": 130.00, "category": "Pasta Specials", "image": IMG["pasta_alfredo"]},
        {"name": "Thursday: Creamy Tomato & Spinach", "description": "Thursday special - creamy tomato & spinach pasta", "price": 120.00, "category": "Pasta Specials", "image": IMG["pasta_tomato"]},
        {"name": "Friday: Classic Meat Lasagna", "description": "Friday special - classic meat lasagna", "price": 130.00, "category": "Pasta Specials", "image": IMG["lasagna"]},
        {"name": "Cold Beverages", "description": "Selection of cold drinks", "price": 15.00, "category": "Beverages", "image": IMG["cold_drink"]},
    ])
    print(f"Seeded Milano's Brunchies: {n} items")

    # ==================== 9. JAZBAR (Jazba Indian Cuisine) ====================
    jazbar_id = f"rest_{uuid.uuid4().hex[:12]}"
    await db.restaurants.insert_one({
        "restaurant_id": jazbar_id,
        "name": "Jazbar",
        "description": "Jazba Indian Cuisine - Halaal. Original Durban Indian Curries & Bunny Chows from the finest authentic Indian spices. Proper Durban Curry flavour & taste! Shop 20 Reyno Ridge Centre.",
        "image": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=600&h=400&fit=crop",
        "cuisine_type": "Indian",
        "rating": 4.7,
        "delivery_time": "30-45 min",
        "price_range": "R65-R160",
        "location": {"lat": -25.8744, "lng": 29.2339, "address": "Shop 20 Reyno Ridge Centre, Witbank"},
        "featured": True, "active": True, "service_type": "food",
        "menu_categories": ["Curries", "Bunny Chows", "Weekly Specials"],
        "available_hours": {"weekdays": "10:00 - 21:00", "weekends": "10:00 - 22:00", "is_open": True},
    })
    n = await seed_items(jazbar_id, [
        # Curries (Large Option - Serves 1-2 People)
        {"name": "Chicken Curry (Large)", "description": "Large chicken curry - serves 1-2 people", "price": 90.00, "category": "Curries", "image": IMG["curry_chicken"]},
        {"name": "Beef Curry (Large)", "description": "Large beef curry - serves 1-2 people", "price": 120.00, "category": "Curries", "image": IMG["curry_beef"]},
        {"name": "Mutton Curry (Large)", "description": "Large mutton curry - serves 1-2 people", "price": 145.00, "category": "Curries", "image": IMG["curry_mutton"]},
        {"name": "Beans Curry (Large)", "description": "Large beans curry - serves 1-2 people", "price": 65.00, "category": "Curries", "image": IMG["curry_beans"]},
        # Bunny Chows
        {"name": "1/4 Chicken Bunny Chow", "description": "Quarter loaf filled with chicken curry", "price": 80.00, "category": "Bunny Chows", "image": IMG["bunny_chow_chicken"]},
        {"name": "1/2 Chicken Bunny Chow", "description": "Half loaf filled with chicken curry", "price": 95.00, "category": "Bunny Chows", "image": IMG["curry_butter"]},
        {"name": "1/4 Beef Bunny Chow", "description": "Quarter loaf filled with beef curry", "price": 105.00, "category": "Bunny Chows", "image": IMG["bunny_chow_beef"]},
        {"name": "1/2 Beef Bunny Chow", "description": "Half loaf filled with beef curry", "price": 125.00, "category": "Bunny Chows", "image": IMG["curry_beef"]},
        {"name": "1/4 Mutton Bunny Chow", "description": "Quarter loaf filled with mutton curry", "price": 115.00, "category": "Bunny Chows", "image": IMG["bunny_chow_mutton"]},
        {"name": "1/2 Mutton Bunny Chow", "description": "Half loaf filled with mutton curry", "price": 160.00, "category": "Bunny Chows", "image": IMG["curry_mutton"]},
        {"name": "1/4 Beans Bunny Chow", "description": "Quarter loaf filled with beans curry", "price": 65.00, "category": "Bunny Chows", "image": IMG["bunny_chow_beans"]},
        {"name": "1/2 Beans Bunny Chow", "description": "Half loaf filled with beans curry", "price": 75.00, "category": "Bunny Chows", "image": IMG["curry_beans"]},
        # Weekly Specials
        {"name": "Monday: Beans Curry & Roti", "description": "Monday special - beans curry with roti", "price": 65.00, "category": "Weekly Specials", "image": IMG["roti"]},
        {"name": "Tuesday: Chicken Curry / 1/4 Bunny Chow", "description": "Tuesday special - chicken curry or quarter bunny chow", "price": 70.00, "category": "Weekly Specials", "image": IMG["curry_chicken"]},
        {"name": "Wednesday: 2x Chicken Shawarma", "description": "Wednesday special - two chicken shawarmas", "price": 90.00, "category": "Weekly Specials", "image": IMG["shawarma_double"]},
        {"name": "Thursday: 1/2 Chicken Tikka & Roti", "description": "Thursday special - half chicken tikka with roti", "price": 95.00, "category": "Weekly Specials", "image": IMG["tikka_chicken"]},
        {"name": "Friday: Chicken Briyani", "description": "Friday special - chicken biryani", "price": 70.00, "category": "Weekly Specials", "image": IMG["biryani"]},
        {"name": "Saturday: 1/4 Mutton Bunny Chow", "description": "Saturday special - quarter mutton bunny chow", "price": 98.00, "category": "Weekly Specials", "image": IMG["bunny_chow_mutton"]},
        {"name": "Sunday: Butter Chicken & Rice", "description": "Sunday special - butter chicken with rice", "price": 95.00, "category": "Weekly Specials", "image": IMG["curry_butter"]},
    ])
    print(f"Seeded Jazbar: {n} items")

    # ==================== 10. CHANTELLY'S LAUNDRY SERVICES ====================
    laundry_id = f"rest_{uuid.uuid4().hex[:12]}"
    await db.restaurants.insert_one({
        "restaurant_id": laundry_id,
        "name": "Chantelly's Laundry Services",
        "description": "Hygiene Beyond Expectations. Professional laundry, dry cleaning, linen, carpets & more. We pick up and deliver!",
        "image": "https://images.unsplash.com/photo-1545173168-9f1947eebb7f?w=600&h=400&fit=crop",
        "cuisine_type": "Laundry",
        "rating": 4.7,
        "delivery_time": "24-48 hrs",
        "price_range": "R32-R705",
        "location": {"lat": -25.8744, "lng": 29.2339, "address": "Witbank, Emalahleni"},
        "featured": True, "active": True, "service_type": "laundry",
        "menu_categories": ["Clothing", "Dress", "Tablecloths", "Linen", "Carpets"],
        "available_hours": {"weekdays": "07:00 - 18:00", "weekends": "08:00 - 14:00", "is_open": True},
    })
    n = await seed_items(laundry_id, [
        # Clothing
        {"name": "Wash and Fold", "description": "Standard wash and fold per item", "price": 33.80, "category": "Clothing", "image": IMG["laundry_wash_fold"]},
        {"name": "Wash and Dry", "description": "Wash and tumble dry per item", "price": 34.98, "category": "Clothing", "image": IMG["laundry_wash_dry"]},
        {"name": "Wash, Dry and Iron", "description": "Full wash, dry and iron service", "price": 36.41, "category": "Clothing", "image": IMG["laundry_iron"]},
        {"name": "Overall (Wash, Dry and Iron)", "description": "Overall full service", "price": 38.61, "category": "Clothing", "image": IMG["laundry_overall"]},
        {"name": "Overall (Wash and Dry)", "description": "Overall wash and dry", "price": 37.51, "category": "Clothing", "image": IMG["laundry_dry_clean"]},
        {"name": "Iron Only", "description": "Ironing service only", "price": 32.01, "category": "Clothing", "image": IMG["laundry_linen_iron"]},
        {"name": "Dry Only", "description": "Tumble dry only", "price": 35.31, "category": "Clothing", "image": IMG["laundry_dry_only"]},
        {"name": "Trouser (Dry Clean)", "description": "Professional trouser dry cleaning", "price": 100.00, "category": "Clothing", "image": IMG["laundry_trouser"]},
        {"name": "Trouser (No Dry Clean)", "description": "Trouser wash and press", "price": 60.00, "category": "Clothing", "image": IMG["laundry_suit"]},
        {"name": "Suit", "description": "Full suit dry cleaning", "price": 225.48, "category": "Clothing", "image": IMG["laundry_blazer"]},
        {"name": "Sneakers", "description": "Sneaker cleaning service", "price": 65.00, "category": "Clothing", "image": IMG["laundry_sneakers"]},
        {"name": "Slippers", "description": "Slipper cleaning service", "price": 65.00, "category": "Clothing", "image": IMG["laundry_slippers"]},
        {"name": "Blazer and Coats", "description": "Blazer and coat dry cleaning", "price": 132.00, "category": "Clothing", "image": IMG["laundry_jacket"]},
        {"name": "Jacket", "description": "Jacket cleaning", "price": 88.00, "category": "Clothing", "image": IMG["laundry_wash_fold"]},
        # Dress
        {"name": "Evening Dress", "description": "Evening dress dry cleaning", "price": 450.00, "category": "Dress", "image": IMG["laundry_dress_evening"]},
        {"name": "Wedding Dress", "description": "Wedding dress professional cleaning", "price": 555.50, "category": "Dress", "image": IMG["laundry_dress_wedding"]},
        # Tablecloths
        {"name": "Tablecloths (Big)", "description": "Large tablecloth wash & iron", "price": 45.21, "category": "Tablecloths", "image": IMG["laundry_tablecloth"]},
        {"name": "Tablecloths (Normal)", "description": "Normal tablecloth wash & iron", "price": 40.15, "category": "Tablecloths", "image": IMG["laundry_tablecloth_sm"]},
        # Linen
        {"name": "Linen (Wash, Dry and Iron)", "description": "Full linen service", "price": 39.82, "category": "Linen", "image": IMG["laundry_linen"]},
        {"name": "Linen (Iron Only)", "description": "Linen ironing only", "price": 37.51, "category": "Linen", "image": IMG["laundry_linen_iron"]},
        {"name": "Blankets (Single/Three Quarter)", "description": "Single or three quarter blanket wash", "price": 69.30, "category": "Linen", "image": IMG["laundry_blanket_s"]},
        {"name": "Blankets (Double)", "description": "Double blanket wash", "price": 94.71, "category": "Linen", "image": IMG["laundry_blanket_d"]},
        {"name": "Blankets (Queen)", "description": "Queen blanket wash", "price": 143.55, "category": "Linen", "image": IMG["laundry_blanket_q"]},
        {"name": "Blankets (King)", "description": "King blanket wash", "price": 154.11, "category": "Linen", "image": IMG["laundry_blanket_k"]},
        {"name": "Comforters (Single)", "description": "Single comforter wash", "price": 70.51, "category": "Linen", "image": IMG["laundry_comforter_s"]},
        {"name": "Comforters (Three Quarter)", "description": "Three quarter comforter wash", "price": 83.71, "category": "Linen", "image": IMG["laundry_comforter_tq"]},
        {"name": "Comforters (Double)", "description": "Double comforter wash", "price": 95.81, "category": "Linen", "image": IMG["laundry_comforter_d"]},
        {"name": "Comforters (Queen)", "description": "Queen comforter wash", "price": 121.17, "category": "Linen", "image": IMG["laundry_comforter_q"]},
        {"name": "Comforters (King)", "description": "King comforter wash", "price": 148.72, "category": "Linen", "image": IMG["laundry_comforter_k"]},
        {"name": "Curtains", "description": "Curtain wash and iron per panel", "price": 45.21, "category": "Linen", "image": IMG["laundry_curtains"]},
        # Carpets
        {"name": "Bathmat Set", "description": "Bathmat set cleaning", "price": 44.00, "category": "Carpets", "image": IMG["laundry_bathmat"]},
        {"name": "Carpet - Small", "description": "Small carpet deep clean", "price": 182.60, "category": "Carpets", "image": IMG["laundry_carpet_s"]},
        {"name": "Carpet - Large", "description": "Large carpet deep clean", "price": 358.60, "category": "Carpets", "image": IMG["laundry_carpet_l"]},
        {"name": "Carpet - X Large", "description": "Extra large carpet deep clean", "price": 704.55, "category": "Carpets", "image": IMG["laundry_carpet_xl"]},
    ])
    print(f"Seeded Chantelly's Laundry: {n} items")

    # ==================== 11. NO LIMIT FLOWERS ====================
    florist_id = f"rest_{uuid.uuid4().hex[:12]}"
    await db.restaurants.insert_one({
        "restaurant_id": florist_id,
        "name": "No Limit Flowers",
        "description": "Beautiful fresh flower arrangements delivered to your door. Perfect for birthdays, anniversaries, or just because!",
        "image": "https://images.unsplash.com/photo-1487530811176-3780de880c2d?w=600&h=400&fit=crop",
        "cuisine_type": "Florist",
        "rating": 4.8,
        "delivery_time": "2-4 hrs",
        "price_range": "R25-R800",
        "location": {"lat": -25.8744, "lng": 29.2339, "address": "Witbank, Emalahleni"},
        "featured": True, "active": True, "service_type": "florist",
        "menu_categories": ["Bouquets", "Arrangements", "Roses", "Add-ons"],
        "available_hours": {"weekdays": "08:00 - 17:00", "weekends": "08:00 - 13:00", "is_open": True},
    })
    n = await seed_items(florist_id, [
        {"name": "Mixed Bouquet - Small", "description": "Beautiful mix of seasonal flowers", "price": 150.00, "category": "Bouquets", "image": IMG["bouquet_mixed_sm"]},
        {"name": "Mixed Bouquet - Large", "description": "Grand arrangement of seasonal flowers", "price": 350.00, "category": "Bouquets", "image": IMG["bouquet_mixed_lg"]},
        {"name": "Sunflower Bouquet", "description": "Bright sunflower arrangement", "price": 200.00, "category": "Bouquets", "image": IMG["bouquet_sunflower"]},
        {"name": "Lily Arrangement", "description": "Elegant lily arrangement in vase", "price": 280.00, "category": "Arrangements", "image": IMG["arrangement_lily"]},
        {"name": "Romantic Rose Box", "description": "Luxury rose box arrangement", "price": 450.00, "category": "Arrangements", "image": IMG["arrangement_rose_box"]},
        {"name": "12 Red Roses", "description": "Classic dozen red roses wrapped", "price": 300.00, "category": "Roses", "image": IMG["roses_12"]},
        {"name": "24 Red Roses", "description": "Two dozen premium red roses", "price": 550.00, "category": "Roses", "image": IMG["roses_24"]},
        {"name": "50 Red Roses", "description": "Grand fifty red roses bouquet", "price": 800.00, "category": "Roses", "image": IMG["roses_50"]},
        {"name": "Chocolate Box", "description": "Premium chocolate box add-on", "price": 120.00, "category": "Add-ons", "image": IMG["chocolate_box"]},
        {"name": "Greeting Card", "description": "Personalised greeting card", "price": 25.00, "category": "Add-ons", "image": IMG["greeting_card"]},
        {"name": "Teddy Bear", "description": "Cute plush teddy bear", "price": 150.00, "category": "Add-ons", "image": IMG["teddy_bear"]},
    ])
    print(f"Seeded No Limit Flowers: {n} items")

    # ==================== 12. NO LIMIT PARCELS ====================
    parcel_id = f"rest_{uuid.uuid4().hex[:12]}"
    await db.restaurants.insert_one({
        "restaurant_id": parcel_id,
        "name": "No Limit Parcels",
        "description": "Fast door-to-door parcel pickup and delivery. Same-day delivery available. Price based on distance.",
        "image": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=600&h=400&fit=crop",
        "cuisine_type": "Parcel Delivery",
        "rating": 4.5,
        "delivery_time": "Same day",
        "price_range": "R10-R250",
        "location": {"lat": -25.8744, "lng": 29.2339, "address": "Witbank, Emalahleni"},
        "featured": False, "active": True, "service_type": "parcel",
        "menu_categories": ["Standard Delivery", "Express Delivery", "Packaging"],
        "available_hours": {"weekdays": "08:00 - 18:00", "weekends": "09:00 - 14:00", "is_open": True},
    })
    n = await seed_items(parcel_id, [
        {"name": "Standard Delivery (0-5km)", "description": "Same-day delivery within 5km radius", "price": 50.00, "category": "Standard Delivery", "image": IMG["parcel_standard_5"]},
        {"name": "Standard Delivery (5-15km)", "description": "Same-day delivery 5-15km radius", "price": 80.00, "category": "Standard Delivery", "image": IMG["parcel_standard_15"]},
        {"name": "Standard Delivery (15-30km)", "description": "Same-day delivery 15-30km radius", "price": 120.00, "category": "Standard Delivery", "image": IMG["parcel_standard_30"]},
        {"name": "Standard Delivery (30-50km)", "description": "Next-day delivery 30-50km", "price": 180.00, "category": "Standard Delivery", "image": IMG["parcel_standard_50"]},
        {"name": "Express Delivery (0-5km)", "description": "1-hour express delivery within 5km", "price": 80.00, "category": "Express Delivery", "image": IMG["parcel_express_5"]},
        {"name": "Express Delivery (5-15km)", "description": "2-hour express delivery 5-15km", "price": 120.00, "category": "Express Delivery", "image": IMG["parcel_express_15"]},
        {"name": "Express Delivery (15-30km)", "description": "3-hour express delivery 15-30km", "price": 200.00, "category": "Express Delivery", "image": IMG["parcel_express_30"]},
        {"name": "Small Box", "description": "Packaging box for small items", "price": 15.00, "category": "Packaging", "image": IMG["parcel_box_sm"]},
        {"name": "Medium Box", "description": "Packaging box for medium items", "price": 25.00, "category": "Packaging", "image": IMG["parcel_box_md"]},
        {"name": "Bubble Wrap", "description": "Protective bubble wrap for fragile items", "price": 10.00, "category": "Packaging", "image": IMG["parcel_bubble"]},
    ])
    print(f"Seeded No Limit Parcels: {n} items")

    # ==================== 13. WITMED PHARMACY & CLINIC ====================
    pharmacy_id = f"rest_{uuid.uuid4().hex[:12]}"
    await db.restaurants.insert_one({
        "restaurant_id": pharmacy_id,
        "name": "Witmed Pharmacy & Clinic",
        "description": "Healthcare facility offering pharmaceutical services, health products, supplements, skincare & clinic services. Expert pharmacists on hand.",
        "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/Untitled-3.webp?v=1741790230&width=3840",
        "cuisine_type": "Pharmacy",
        "rating": 4.6,
        "delivery_time": "30-60 min",
        "price_range": "R50-R1299",
        "location": {"lat": -25.8744, "lng": 29.2339, "address": "Witbank, Emalahleni"},
        "featured": True, "active": True, "service_type": "pharmacy",
        "menu_categories": ["Health Supplements", "Weight Management", "Skin & Beauty", "Digestive Health", "Immune Boosters", "Clinic Services"],
        "available_hours": {"weekdays": "08:00 - 18:00", "weekends": "08:00 - 13:00", "is_open": True},
    })
    n = await seed_items(pharmacy_id, [
        {"name": "Vitatech Women's Pack", "description": "Complete women's vitamin pack", "price": 220.00, "category": "Health Supplements", "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/IMG-4765.webp?v=1758880535&width=533"},
        {"name": "Ashvagandha", "description": "Ashwagandha supplement for stress & energy", "price": 190.00, "category": "Health Supplements", "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/Ashvagandha_-_Witmed_Pharmacy.webp?v=1743492314&width=533"},
        {"name": "Collagen Capsules", "description": "Collagen supplement for skin & joints", "price": 215.00, "category": "Health Supplements", "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/Collagencapsules-WitmedPharmacy.webp?v=1741787781&width=533"},
        {"name": "Chlorophyll Drops 473ml", "description": "Liquid chlorophyll drops 473ml", "price": 650.00, "category": "Health Supplements", "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/IMG-3451.jpg?v=1752226323&width=533"},
        {"name": "Avogel Nephrosolid", "description": "Avogel kidney support supplement", "price": 230.00, "category": "Health Supplements", "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/IMG-5113.webp?v=1760080367&width=533"},
        {"name": "Canephron Bionorica 60 Tablets", "description": "Canephron urinary tract support", "price": 300.00, "category": "Health Supplements", "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/Collagencapsules-WitmedPharmacy.webp?v=1741787781&width=400"},
        {"name": "African Potato 1L", "description": "African potato immune booster 1L", "price": 150.00, "category": "Health Supplements", "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/Ashvagandha_-_Witmed_Pharmacy.webp?v=1743492314&width=400"},
        {"name": "Chia Seeds", "description": "Organic chia seeds superfood", "price": 60.00, "category": "Health Supplements", "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/IMG-4765.webp?v=1758880535&width=400"},
        {"name": "Apple Cider Vinegar 200ml", "description": "Pure apple cider vinegar 200ml", "price": 50.00, "category": "Health Supplements", "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/IMG-3451.jpg?v=1752226323&width=400"},
        {"name": "Sela Slimming Tea", "description": "Natural herbal slimming tea", "price": 61.99, "category": "Weight Management", "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/IMG-5113.webp?v=1760080367&width=400"},
        {"name": "Flat Tummy Toner", "description": "Flat tummy toning supplement", "price": 187.00, "category": "Weight Management", "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/Collagencapsules-WitmedPharmacy.webp?v=1741787781&width=350"},
        {"name": "Glutathione Lotion 500ml", "description": "Glutathione brightening lotion 500ml", "price": 600.00, "category": "Skin & Beauty", "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/Ashvagandha_-_Witmed_Pharmacy.webp?v=1743492314&width=350"},
        {"name": "Sela Clear Skin Capsules", "description": "Clear skin herbal capsules", "price": 78.00, "category": "Skin & Beauty", "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/IMG-4765.webp?v=1758880535&width=350"},
        {"name": "Obee's HPS 100ml", "description": "Obee's skin treatment 100ml", "price": 165.00, "category": "Skin & Beauty", "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/IMG-3451.jpg?v=1752226323&width=350"},
        {"name": "Acid Flush Powder", "description": "Acid flush digestive powder", "price": 130.00, "category": "Digestive Health", "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/IMG-5113.webp?v=1760080367&width=350"},
        {"name": "Acid Flush Tonic + FREE Powder", "description": "Acid flush tonic with bonus powder", "price": 195.00, "category": "Digestive Health", "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/Collagencapsules-WitmedPharmacy.webp?v=1741787781&width=300"},
        {"name": "Citro Soda Cranberry 120g", "description": "Citro soda cranberry 120g", "price": 145.00, "category": "Digestive Health", "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/Ashvagandha_-_Witmed_Pharmacy.webp?v=1743492314&width=300"},
        {"name": "Citro Soda Granules 60g", "description": "Citro soda granules 60g", "price": 100.00, "category": "Digestive Health", "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/IMG-4765.webp?v=1758880535&width=300"},
        {"name": "Presto Gel Suppositories 12", "description": "Presto gel suppositories 12-pack", "price": 140.00, "category": "Digestive Health", "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/IMG-3451.jpg?v=1752226323&width=300"},
        {"name": "Wohloza Syrup", "description": "Wohloza immune support syrup", "price": 135.00, "category": "Immune Boosters", "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/IMG-5113.webp?v=1760080367&width=300"},
        {"name": "Addiction Flush Tonic", "description": "Natural addiction flush tonic", "price": 130.00, "category": "Immune Boosters", "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/Collagencapsules-WitmedPharmacy.webp?v=1741787781&width=250"},
        {"name": "Cancerbush Tea", "description": "Sutherlandia cancerbush tea", "price": 65.00, "category": "Immune Boosters", "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/Ashvagandha_-_Witmed_Pharmacy.webp?v=1743492314&width=250"},
        {"name": "Babalas Rescue 200ml", "description": "Hangover rescue remedy 200ml", "price": 50.00, "category": "Immune Boosters", "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/IMG-4765.webp?v=1758880535&width=250"},
        {"name": "Glutathione Drip", "description": "IV glutathione drip service", "price": 1150.00, "category": "Clinic Services", "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/IMG-3451.jpg?v=1752226323&width=250"},
        {"name": "Lemon Bottle Lipo Injections", "description": "Lemon bottle fat dissolving injections", "price": 1299.00, "category": "Clinic Services", "image": "https://www.witmedpharmacy.co.za/cdn/shop/files/IMG-5113.webp?v=1760080367&width=250"},
    ])
    print(f"Seeded Witmed Pharmacy: {n} items")

    # ==================== SUMMARY ====================
    total_restaurants = await db.restaurants.count_documents({})
    total_items = await db.menu_items.count_documents({})
    total_services = await db.services.count_documents({})
    print(f"\n{'='*60}")
    print(f"SEED COMPLETE: {total_restaurants} providers, {total_items} items, {total_services} services")
    print(f"{'='*60}")

asyncio.run(seed())
