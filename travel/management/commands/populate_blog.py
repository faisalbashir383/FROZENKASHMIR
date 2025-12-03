from django.core.management.base import BaseCommand
from travel.models import BlogCategory, BlogPost

class Command(BaseCommand):
    help = 'Populate blog with 20 travel posts'

    def handle(self, *args, **kwargs):
        # Create categories
        categories_data = [
            {'name': 'Travel Tips', 'slug': 'travel-tips', 'description': 'Essential travel tips for Kashmir'},
            {'name': 'Destination Guides', 'slug': 'destination-guides', 'description': 'Detailed guides to Kashmir destinations'},
            {'name': 'Adventure Stories', 'slug': 'adventure-stories', 'description': 'Thrilling adventure experiences'},
            {'name': 'Culture & Local Life', 'slug': 'culture-local-life', 'description': 'Kashmir culture and traditions'},
            {'name': 'Photography', 'slug': 'photography', 'description': 'Photography tips for Kashmir'},
            {'name': 'Seasonal Activities', 'slug': 'seasonal-activities', 'description': 'Activities by season'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            cat, created = BlogCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name'], 'description': cat_data['description']}
            )
            categories[cat_data['slug']] = cat
            if created:
                self.stdout.write(f'Created category: {cat.name}')

        # Create 20 blog posts
        posts_data = [
            {
                'title': '10 Essential Tips for Your First Kashmir Trip',
                'slug': '10-essential-tips-first-kashmir-trip',
                'category': 'travel-tips',
                'featured_image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200',
                'excerpt': 'Planning your first trip to Kashmir? Here are 10 essential tips to make your journey unforgettable.',
                'content': 'Kashmir, often called Paradise on Earth, requires some planning to ensure a smooth experience. 1) Best time to visit is April-October for pleasant weather. 2) Book accommodations in advance, especially during peak season. 3) Carry warm clothing even in summer. 4) Try local cuisine like Wazwan and Kahwa. 5) Respect local customs and dress modestly. 6) Hire local guides for trekking. 7) Keep your phone charged and carry power banks. 8) Stay hydrated at high altitudes. 9) Book houseboats on Dal Lake in advance. 10) Always carry your ID proof.',
                'tags': 'kashmir, travel tips, first time, planning',
                'meta_description': '10 essential tips for planning your first trip to Kashmir. Travel advice for first-time visitors.'
            },
            {
                'title': 'Gulmarg: The Meadow of Flowers - Complete Guide',
                'slug': 'gulmarg-meadow-flowers-complete-guide',
                'category': 'destination-guides',
                'featured_image': 'https://images.unsplash.com/photo-1676441019594-07142b925bc2?w=1200',
                'excerpt': 'Discover Gulmarg, Kashmir\'s premier ski resort and summer paradise. Everything you need to know.',
                'content': 'Gulmarg sits at 2,650 meters and transforms with seasons. In winter, it\'s Asia\'s premier skiing destination with world-class slopes. The Gulmarg Gondola, one of the highest cable cars globally, offers breathtaking views. In summer, meadows bloom with wildflowers. Activities include skiing, snowboarding, golfing at the world\'s highest green golf course, and trekking to Alpather Lake. Stay at hotels ranging from luxury to budget. Best time: December-March for snow sports, April-June for flowers.',
                'tags': 'gulmarg, skiing, gondola, flowers, kashmir',
                'meta_description': 'Complete travel guide to Gulmarg, Kashmir. Skiing, gondola rides, and summer activities.'
            },
            {
                'title': 'Trekking to Tarsar Marsar Lakes: An Adventure Guide',
                'slug': 'trekking-tarsar-marsar-lakes-adventure',
                'category': 'adventure-stories',
                'featured_image': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200',
                'excerpt': 'Trek to the stunning twin alpine lakes of Tarsar and Marsar in Kashmir. A moderate 7-day adventure.',
                'content': 'The Tarsar Marsar trek is a moderate 48km journey through meadows, forests, and alpine lakes. Starting from Aru Valley, you\'ll trek through Lidderwat, cross mountain passes, and camp beside pristine lakes. Day 1: Aru to Lidderwat. Day 2: Lidderwat to Shekwas. Day 3: Acclimatization. Day 4: Tarsar Lake. Day 5: Marsar Lake. Day 6-7: Return. Best season: June-September. Fitness required: moderate. Carry warm gear, the altitude reaches 4,000m. Hire local guides and porters from Aru.',
                'tags': 'trekking, tarsar marsar, adventure, lakes, kashmir',
                'meta_description': 'Complete guide to Tarsar Marsar trek in Kashmir. 7-day alpine lake adventure.'
            },
            {
                'title': 'Wazwan: The Royal Feast of Kashmir',
                'slug': 'wazwan-royal-feast-kashmir',
                'category': 'culture-local-life',
                'featured_image': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=1200',
                'excerpt': 'Explore Wazwan, Kashmir\'s legendary multi-course meal. A culinary journey through tradition.',
                'content': 'Wazwan is not just a meal; it\'s a ceremony. This 36-course feast, prepared by master chefs called Wazas, represents Kashmiri hospitality. Served in copper vessels called traami, 4 people share from one plate. Star dishes include Rista (minced mutton balls), Rogan Josh, Tabak Maaz (fried ribs), and Gushtaba (the final dish). The meal begins with Rista and ends with sweet Phirni. Experiencing Wazwan is essential to understanding Kashmiri culture. Many restaurants in Srinagar offer mini Wazwan for tourists.',
                'tags': 'wazwan, kashmiri food, cuisine, culture, tradition',
                'meta_description': 'Discover Wazwan, Kashmir\'s legendary 36-course feast. Traditional Kashmiri cuisine guide.'
            },
            {
                'title': 'Photography Guide: Capturing Kashmir\'s Beauty',
                'slug': 'photography-guide-capturing-kashmir-beauty',
                'category': 'photography',
                'featured_image': 'https://images.unsplash.com/photo-1452421822248-d4c2b47f0c81?w=1200',
                'excerpt': 'Tips and tricks for photographing Kashmir\'s stunning landscapes, from Dal Lake to mountain peaks.',
                'content': 'Kashmir is a photographer\'s paradise. Golden hour at Dal Lake creates mirror reflections. For landscapes, carry wide-angle lenses (16-35mm). Capture Shikara boats at sunrise. In Gulmarg, photograph snow-covered peaks with polarizing filters. Visit Betaab Valley for waterfall shots. Pahalgam\'s Lidder River offers long-exposure opportunities. For cultural shots, visit local markets. Respect locals before photographing people. Best light: early morning and evening. Carry extra batteries (cold drains power). Use graduated ND filters for sky-ground contrast. Spring flowers in Tulip Garden need macro lenses.',
                'tags': 'photography, kashmir, landscapes, travel photography, tips',
                'meta_description': 'Photography guide for Kashmir. Tips for capturing stunning landscapes and cultural moments.'
            },
            {
                'title': 'Winter Wonderland: Kashmir in Snow Season',
                'slug': 'winter-wonderland-kashmir-snow-season',
                'category': 'seasonal-activities',
                'featured_image': 'https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5?w=1200',
                'excerpt': 'Experience Kashmir covered in snow. Winter activities, festivals, and travel tips for December to February.',
                'content': 'Winter transforms Kashmir into a snow wonderland. December-February sees heavy snowfall. Gulmarg becomes a skiing paradise. Try snowboarding, sledging, and snow biking. Visit frozen Dal Lake for unique ice skating. Explore Doodhpathri covered in white. Winter festivals celebrate local culture. Stay warm in traditional Kangri (fire pots). Enjoy hot Kahwa tea and local cuisine. Book hotels with heating. Roads may close due to snow, plan flexibly. Carry warm layers, thermals, and waterproof boots. Photography opportunities are stunning but bring lens warmers.',
                'tags': 'winter kashmir, snow, skiing, seasonal, december',
                'meta_description': 'Kashmir in winter: Snow activities, skiing, and winter travel guide for December-February.'
            },
            {
                'title': 'Dal Lake Houseboats: A Unique Stay Experience',
                'slug': 'dal-lake-houseboats-unique-stay',
                'category': 'destination-guides',
                'featured_image': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=1200',
                'excerpt': 'Staying in a traditional houseboat on Dal Lake is a quintessential Kashmir experience. Here\'s everything you need to know.',
                'content': 'Dal Lake houseboats are floating palaces built from cedar wood. Dating back to British era, these offer luxury on water. Each houseboat has bedrooms, living rooms, and verandas. Categories range from deluxe to budget. Wake up to mountain views and Shikara vendors. Enjoy traditional Kashmiri breakfast onboard. Take Shikara rides to floating gardens and markets. Best time: March-October. Book directly or through agencies. Prices vary by season and amenities. Experience includes sunset views, peaceful nights, and unique hospitality. Most houseboats are in Nigeen Lake and Dal Lake boulevards.',
                'tags': 'dal lake, houseboat, accommodation, srinagar, kashmir',
                'meta_description': 'Guide to staying in Dal Lake houseboats. Traditional Kashmir houseboat experience.'
            },
            {
                'title': 'Pahalgam: The Valley of Shepherds - Travel Guide',
                'slug': 'pahalgam-valley-shepherds-travel-guide',
                'category': 'destination-guides',
                'featured_image': 'https://images.unsplash.com/photo-1701957494338-95527b753a7f?w=1200',
                'excerpt': 'Explore Pahalgam, a serene valley perfect for nature lovers and adventure seekers alike.',
                'content': 'Pahalgam, at 2,740m, is where Bollywood meets nature. The Lidder River flows through pine forests creating picture-perfect scenery. Visit Betaab Valley (named after the movie), Aru Valley for trekking base, and Chandanwari (Amarnath Yatra start point). Activities include river rafting, trout fishing, horseback riding, and trekking. The main market offers local handicrafts. Stay in hotels or riverside camps. Best time: April-October. Day trips possible from Srinagar (90km). Winter brings snow. Try local restaurants for authentic food. Golf course available for enthusiasts.',
                'tags': 'pahalgam, betaab valley, aru valley, trekking, kashmir',
                'meta_description': 'Complete Pahalgam travel guide. Valley of Shepherds attractions and activities.'
            },
            {
                'title': 'Kashmiri Handicrafts: A Shopper\'s Paradise',
                'slug': 'kashmiri-handicrafts-shoppers-paradise',
                'category': 'culture-local-life',
                'featured_image': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=1200',
                'excerpt': 'Discover Kashmir\'s rich handicraft tradition. From Pashmina shawls to hand-knotted carpets.',
                'content': 'Kashmir handicrafts are world-renowned. Pashmina shawls are ultra-soft luxury made from Himalayan goat wool. Authentic Pashmina costs significant money, beware of fakes. Hand-knotted silk carpets require months of work. Papier-mâché products showcase intricate designs. Walnut wood carvings are unique souvenirs. Crewel embroidery adorns fabrics beautifully. Shop at government emporia for guaranteed quality. Lal Chowk and Polo View markets offer variety. Bargaining is expected. For carpets, visit showrooms with certificates. Saffron from Pampore is pure and aromatic. Carry items carefully or use shipping services.',
                'tags': 'handicrafts, pashmina, shopping, carpets, kashmir',
                'meta_description': 'Guide to Kashmir handicrafts. Pashmina shawls, carpets, and authentic shopping tips.'
            },
            {
                'title': 'Sonamarg: The Meadow of Gold Adventure',
                'slug': 'sonamarg-meadow-gold-adventure',
                'category': 'destination-guides',
                'featured_image': 'https://images.unsplash.com/photo-1643449415972-87d4cfe882a1?w=1200',
                'excerpt': 'Sonamarg offers golden meadows, glacier views, and thrilling adventures in the Himalayas.',
                'content': 'Sonamarg at 2,800m is the last major town before Ladakh. The name means "Meadow of Gold" due to yellow flowers in spring. Thajiwas Glacier trek is popular (7km, easy). Hire ponies or trek on foot through snow fields even in summer. Sindh River offers white-water rafting. Visit Zero Point (89km, permit required). Camping in meadows is spectacular. Trout fishing permits available. Day trip from Srinagar possible (80km, 2 hours). Accommodation limited, mostly seasonal camps and hotels. Road closes in winter. Best visit: May-September. Carry warm clothes, altitude sickness possible.',
                'tags': 'sonamarg, glacier, trekking, meadows, kashmir',
                'meta_description': 'Sonamarg travel guide. Thajiwas Glacier trek and adventure activities.'
            },
            {
                'title': 'Spring in Kashmir: Tulip Garden and Cherry Blossoms',
                'slug': 'spring-kashmir-tulip-garden-cherry-blossoms',
                'category': 'seasonal-activities',
                'featured_image': 'https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=1200',
                'excerpt': 'Experience spring magic in Kashmir with Asia\'s largest tulip garden and blooming orchards.',
                'content': 'Spring (March-May) brings Kashmir to life. Indira Gandhi Memorial Tulip Garden in Srinagar displays over 1.5 million tulips across 70+ varieties. Open only in April for 2-3 weeks. Cherry and almond blossoms blanket orchards in Badamwari and Naseem Bagh. Mughal Gardens (Nishat, Shalimar, Chashme Shahi) are at their best. Temperature is pleasant (15-25°C). Book early, peak season prices apply. Best photography opportunities. Celebrate local spring festivals. Markets overflow with fresh fruits. Perfect time for houseboats and Shikara rides. Fewer tourists than summer. Carry light woolens for evenings.',
                'tags': 'spring, tulip garden, flowers, seasonal, kashmir',
                'meta_description': 'Kashmir in spring. Tulip garden blooms, cherry blossoms, and best time to visit.'
            },
            {
                'title': 'Amarnath Yatra: Sacred Pilgrimage Guide',
                'slug': 'amarnath-yatra-sacred-pilgrimage-guide',
                'category': 'culture-local-life',
                'featured_image': 'https://images.unsplash.com/photo-1548625149-d8c38a3d7e9d?w=1200',
                'excerpt': 'Complete guide to the sacred Amarnath Yatra, one of Hinduism\'s most revered pilgrimages.',
                'content': 'Amarnath Cave houses a natural ice Shiva Lingam at 3,880m. The annual pilgrimage (July-August) attracts hundreds of thousands. Two routes: Traditional Pahalgam (36-48km, 3-5 days) and shorter Baltal (14km, 1 day). Registration mandatory through www.shriamarnathjishrine.com. Health certificate required. Permits allocated through lottery. Facilities include camps, food, medical stations, and helicopter services. Trek is challenging, requires fitness. Carry oxygen, warm clothes, rain gear. Ponies and palanquins available. Respect religious sentiments. Free langar (community kitchen) provided. Experience is spiritually transformative. Non-pilgrims need special permits to visit the region.',
                'tags': 'amarnath, yatra, pilgrimage, spiritual, kashmir',
                'meta_description': 'Amarnath Yatra complete guide. Sacred pilgrimage to Amarnath Cave in Kashmir.'
            },
            {
                'title': 'Rafting in Kashmir: Lidder and Sindh Rivers',
                'slug': 'rafting-kashmir-lidder-sindh-rivers',
                'category': 'adventure-stories',
                'featured_image': 'https://images.unsplash.com/photo-1527004013197-933c4bb611b3?w=1200',
                'excerpt': 'White-water rafting adventures on Kashmir\'s pristine rivers. An adrenaline-pumping experience.',
                'content': 'Kashmir offers excellent rafting from April to September. Lidder River in Pahalgam: Grade II-III rapids, 12km stretch from Pahalgam to Aishmuqam. Suitable for beginners with guides. Sindh River near Sonamarg: Grade III-IV rapids, more challenging, 15km stretch. Both rivers flow through scenic valleys. Professional operators provide equipment and guides. Safety briefings mandatory. Wear life jackets and helmets. Book certified operators only. Best months: May-June (high water). Cost: ₹500-1500 per person. Combined with camping packages. Age restrictions apply (usually 14+). Photography services available. Experience magnificent mountain views while navigating rapids.',
                'tags': 'rafting, adventure, lidder river, sindh river, kashmir',
                'meta_description': 'White-water rafting in Kashmir. Lidder and Sindh river adventures for all levels.'
            },
            {
                'title': 'Mughal Gardens of Kashmir: Historical Beauty',
                'slug': 'mughal-gardens-kashmir-historical-beauty',
                'category': 'destination-guides',
                'featured_image': 'https://images.unsplash.com/photo-1585737883235-d5ea30bf7133?w=1200',
                'excerpt': 'Explore the magnificent Mughal Gardens of Srinagar, showcasing centuries-old Persian architecture.',
                'content': 'Mughal emperors built terraced gardens in Kashmir following Persian Char Bagh style. Shalimar Bagh (1619): Largest garden, built by Jehangir for Nur Jahan. Three terraces with fountains and lawns. Nishat Bagh: "Garden of Joy" with 12 terraces representing zodiac signs. Stunning Dal Lake views. Chashme Shahi: Smallest royal garden with natural spring. Pari Mahal: Ruined garden palace with city views. Best time: April-October, especially spring. Evening illumination in summer. Entry fees nominal. Photography allowed. Combine visiting all gardens in one day. Located on Dal Lake boulevard. Perfect for picnics and peaceful walks.',
                'tags': 'mughal gardens, shalimar, nishat, heritage, srinagar',
                'meta_description': 'Mughal Gardens of Kashmir guide. Shalimar, Nishat, and Chashme Shahi historical gardens.'
            },
            {
                'title': 'Kashmiri Kahwa: The Traditional Tea Culture',
                'slug': 'kashmiri-kahwa-traditional-tea-culture',
                'category': 'culture-local-life',
                'featured_image': 'https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=1200',
                'excerpt': 'Discover the aromatic Kashmiri Kahwa tea, its preparation, benefits, and cultural significance.',
                'content': 'Kahwa is Kashmir\'s signature green tea infused with saffron, cardamom, cinnamon, and almonds. Served in traditional samovars, it\'s integral to Kashmiri hospitality. Health benefits include digestion aid, metabolism boost, and warmth in cold weather. Preparation: Brew green tea with spices, add saffron strands, garnish with crushed almonds. Sweeten with honey or sugar. Served throughout the day, especially to guests. Buy authentic Kahwa mix from local markets. Different families have secret recipes. Pink salt from Himalayan mines sometimes added. Learn preparation by visiting Kashmiri homes or cafes. Perfect souvenir to take home. Accompanies local breads and cookies.',
                'tags': 'kahwa, tea, kashmiri culture, beverages, tradition',
                'meta_description': 'Kashmiri Kahwa tea guide. Traditional preparation, health benefits, and cultural significance.'
            },
            {
                'title': 'Skiing in Gulmarg: Asia\'s Skiing Paradise',
                'slug': 'skiing-gulmarg-asia-paradise',
                'category': 'seasonal-activities',
                'featured_image': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=1200',
                'excerpt': 'Everything you need to know about skiing in Gulmarg, from slopes to equipment rentals.',
                'content': 'Gulmarg offers some of Asia\'s best skiing from December to March. The Gulmarg Gondola accesses slopes up to 3,980m. Beginner slopes at Kongdori, advanced at Apharwat. Powder snow quality rivals European Alps. Skiing packages include equipment rental, instructors, and lift passes. Rental shops in Gulmarg town. International and Indian instructors available. Helicopter skiing for experts. Safety gear mandatory. Weather can change quickly. Book ski schools in advance during peak season (Jan-Feb). Accommodation book early. Non-skiers can enjoy gondola rides and snow activities. Medical facilities available. Ski season extends into March for late snow.',
                'tags': 'skiing, gulmarg, winter sports, adventure, snow',
                'meta_description': 'Complete skiing guide for Gulmarg, Kashmir. Asia\'s premier ski destination.'
            },
            {
                'title': 'Budget Travel Guide to Kashmir',
                'slug': 'budget-travel-guide-kashmir',
                'category': 'travel-tips',
                'featured_image': 'https://images.unsplash.com/photo-1553531087-e90c0d1656df?w=1200',
                'excerpt': 'Experience Kashmir on a budget. Money-saving tips for accommodation, food, and activities.',
                'content': 'Kashmir can be affordable with planning. Transport: Share taxis cost less than private cars. Group together for better rates. Accommodation: Stay in guest houses (₹500-1000/night) instead of hotels. Hostel dorms available in Srinagar. Food: Eat at local dhabas, avoid tourist restaurants. Try street food (₹50-100). Activities: Public gardens charge nominal fees. Trekking is low-cost. Skip expensive activities like Gondola in peak season. Shopping: Bargain everywhere except government shops. Off-season (Nov-Feb except Dec) offers 50% discounts. Cook in hostel kitchens. Use local buses than tourist buses. Free: Walking tours, sunset at Dal Lake, local markets.',
                'tags': 'budget travel, kashmir, money saving, affordable, tips',
                'meta_description': 'Budget travel guide to Kashmir. Money-saving tips for affordable Kashmir trip.'
            },
            {
                'title': 'Kashmir Honeymoon: Romantic Escapades',
                'slug': 'kashmir-honeymoon-romantic-escapades',
                'category': 'travel-tips',
                'featured_image': 'https://images.unsplash.com/photo-1519802590718-c3fb43956b4b?w=1200',
                'excerpt': 'Plan the perfect Kashmir honeymoon with romantic locations, activities, and itineraries.',
                'content': 'Kashmir is India\'s premier honeymoon destination. Stay in luxury houseboats on Dal Lake. Private Shikara rides at sunset are magical. Gulmarg offers couple gondola rides and snow activities. Pahalgam provides riverside romance and nature walks. Itinerary suggestion: Day 1-2 Srinagar (houseboats, Mughal gardens). Day 3-4 Gulmarg (gondola, snow). Day 5-6 Pahalgam (Betaab Valley, Aru). Day 7 Srinagar departure. Book honeymoon packages with decorations and candlelight dinners. Spring (April-May) perfect for flowers. December-February for snow romance. Photography sessions in traditional Kashmiri attire popular. Private picnics arranged. Couples spa available in luxury hotels.',
                'tags': 'honeymoon, kashmir, romantic, couples, luxury',
                'meta_description': 'Kashmir honeymoon guide. Romantic destinations, activities, and perfect itinerary.'
            },
            {
                'title': 'Exploring Srinagar: The Summer Capital',
                'slug': 'exploring-srinagar-summer-capital',
                'category': 'destination-guides',
                'featured_image': 'https://images.unsplash.com/photo-1564329494258-3f72215ba175?w=1200',
                'excerpt': 'Complete guide to Srinagar, the heart of Kashmir. From Dal Lake to old city charm.',
                'content': 'Srinagar is Kashmir\'s cultural and commercial capital. Dal Lake: Take Shikara rides (₹300-500/hour), visit floating gardens, and stay in houseboats. Old City: Explore narrow lanes, Shah Hamadan mosque, and Jama Masjid. Markets: Lal Chowk for shopping, Residency Road for cafes. Parks: Nishat and Shalimar gardens are must-visits. Food: Try Mughal Darbar, Ahdoos, and street food at Lal Chowk. Accommodation ranges from budget to 5-star. Airport well-connected. Local transport: Auto-rickshaws and taxis. Best time: March-October. Explore beyond tourist spots to old bazaars. Photography at Dal Lake during sunrise. Visit tulip garden in April.',
                'tags': 'srinagar, dal lake, city guide, kashmir, tourism',
                'meta_description': 'Complete Srinagar travel guide. Dal Lake, Mughal gardens, and city attractions.'
            },
            {
                'title': 'Monsoon in Kashmir: Unique Travel Experience',
                'slug': 'monsoon-kashmir-unique-travel',
                'category': 'seasonal-activities',
                'featured_image': 'https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=1200',
                'excerpt': 'Kashmir during monsoon is lush and crowd-free. Discover a different side of paradise.',
                'content': 'July-August brings light rains to Kashmir. The valley turns emerald green. Fewer tourists mean peaceful experiences and better hotel rates (30-50% off). Waterfalls are at their peak. Countryside drives are spectacular. Monsoon is ideal for: Photography (misty mountains), indoor activities (museums, cafes), local cuisine experiences. Consider: Roads may be slippery, carry rain gear, some trek routes close. Benefits: Lower costs, authentic local interactions, lush landscapes. Avoid: Heavy trekking, remote areas during heavy rain. Best for: Budget travelers, photographers, culture enthusiasts. Srinagar, Pahalgam, and Gulmarg accessible. Pack waterproof bags and suitable footwear.',
                'tags': 'monsoon, kashmir, offseason, budget, rain',
                'meta_description': 'Kashmir in monsoon: Off-season travel guide. Lush landscapes and budget-friendly experiences.'
            }
        ]

        for post_data in posts_data:
            cat = categories[post_data['category']]
            post, created = BlogPost.objects.get_or_create(
                slug=post_data['slug'],
                defaults={
                    'title': post_data['title'],
                    'category': cat,
                    'featured_image': post_data['featured_image'],
                    'excerpt': post_data['excerpt'],
                    'content': post_data['content'],
                    'tags': post_data['tags'],
                    'meta_description': post_data['meta_description'],
                    'is_featured': posts_data.index(post_data) < 3  # First 3 are featured
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created post: {post.title}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated blog!'))
