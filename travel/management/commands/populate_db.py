from django.core.management.base import BaseCommand
from travel.models import Destination, Package
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating database...')
        
        # Destinations
        destinations_data = [
            {
                'name': 'Srinagar',
                'description': 'The heart of Kashmir, Srinagar is a city of lakes, gardens, and bridges. Experience the timeless beauty of Dal Lake, the grandeur of Mughal Gardens, and the charm of old city architecture.',
                'highlights': 'Dal Lake Shikara Ride, Mughal Gardens (Nishat, Shalimar), Shankaracharya Temple, Old City Walk, Houseboat Stay',
                'best_time_to_visit': 'April to October for pleasant weather, December to February for snow.'
            },
            {
                'name': 'Gulmarg',
                'description': 'Known as the "Meadow of Flowers", Gulmarg is a premier hill station and skiing destination. It boasts the world\'s highest golf course and the famous Gondola cable car ride.',
                'highlights': 'Gulmarg Gondola (Phase 1 & 2), Skiing & Snowboarding, Alpather Lake, St. Mary\'s Church, Golf Course',
                'best_time_to_visit': 'December to March for snow activities, May to September for lush green meadows.'
            },
            {
                'name': 'Pahalgam',
                'description': 'The "Valley of Shepherds", Pahalgam is a serene retreat situated at the confluence of the streams flowing from the river Lidder and Sheshnag Lake. It is the starting point of the Amarnath Yatra.',
                'highlights': 'Betaab Valley, Aru Valley, Chandanwari, Lidder River Rafting, Pony Rides, Baisaran Valley (Mini Switzerland)',
                'best_time_to_visit': 'April to June for sightseeing, July to September for trekking.'
            },
            {
                'name': 'Sonamarg',
                'description': 'The "Meadow of Gold", Sonamarg is a gateway to the ancient Silk Road. It is known for its thajiwas glacier and as a base for trekking to the high altitude lakes of Vishansar and Krishansar.',
                'highlights': 'Thajiwas Glacier Trek, Zoji La Pass, Zero Point, White Water Rafting, Camping by the river',
                'best_time_to_visit': 'April to September. (Inaccessible in winter due to heavy snow)'
            }
        ]
        
        destinations = {}
        for data in destinations_data:
            dest, created = Destination.objects.get_or_create(
                name=data['name'],
                defaults={
                    'slug': slugify(data['name']),
                    'description': data['description'],
                    'highlights': data['highlights'],
                    'best_time_to_visit': data['best_time_to_visit']
                }
            )
            destinations[data['name']] = dest
            
        # Packages
        packages_data = [
            {
                'title': 'Royal Kashmir Honeymoon Special',
                'category': 'honeymoon',
                'destination': destinations['Srinagar'],
                'duration': '6 Days / 5 Nights',
                'price': 32000,
                'overview': 'Celebrate your love in the "Paradise on Earth". This specially curated honeymoon package offers a romantic houseboat stay, candlelight dinner, and visits to the most enchanting valleys of Kashmir.',
                'itinerary': '''Day 1: Arrival in Srinagar - Welcome to Paradise
Arrive at Srinagar Airport where our representative will welcome you with a warm smile. Transfer to a luxury houseboat on Dal Lake. Enjoy a welcome drink of "Kahwa" (traditional Kashmiri saffron tea). Evening romantic Shikara ride on Dal Lake. Dinner and overnight stay in the houseboat.

Day 2: Srinagar to Gulmarg - The Meadow of Flowers
After breakfast, proceed to Gulmarg (56 kms). Enjoy the scenic drive through pine forests. Board the Gondola Cable Car (world's highest) for breathtaking views of the Apharwat peak. Optional: Skiing or snow activities. Return to Srinagar for overnight stay at a hotel.

Day 3: Srinagar to Pahalgam - Valley of Shepherds
Drive to Pahalgam (96 kms). En route visit Saffron fields at Pampore and Avantipura ruins. In Pahalgam, visit Betaab Valley (famous Bollywood shooting spot) and Aru Valley. Enjoy a romantic walk by the Lidder River. Overnight stay in Pahalgam.

Day 4: Pahalgam Leisure & Sightseeing
Spend the day at leisure in Pahalgam. You can opt for a pony ride to Baisaran Valley (Mini Switzerland) or simply relax amidst nature. Evening return to Srinagar.

Day 5: Srinagar Local Sightseeing - Mughal Grandeur
Visit the famous Mughal Gardens - Nishat Bagh (Garden of Pleasure) and Shalimar Bagh (Abode of Love). Visit the Shankaracharya Temple for a panoramic view of the city. Evening free for shopping at Lal Chowk for Pashmina shawls and handicrafts.

Day 6: Departure
After breakfast, transfer to Srinagar Airport with sweet memories of your Kashmir honeymoon.''',
                'inclusions': '✅ Accommodation in 3 Star Hotels/Houseboat\n✅ Daily Breakfast & Dinner\n✅ 1 Hour Shikara Ride\n✅ All Transfers & Sightseeing by Private Cab\n✅ Welcome Drink on Arrival\n✅ Honeymoon Cake & Candlelight Dinner',
                'exclusions': '❌ Airfare/Train fare\n❌ Lunch\n❌ Gondola Tickets & Pony Rides\n❌ Garden Entrance Fees\n❌ Personal Expenses',
                'is_featured': True,
                'activities': 'sightseeing, romantic, houseboat, shikara ride, nature',
                'difficulty_level': 'easy',
                'group_size_min': 2,
                'group_size_max': 2,
                'popularity_score': 95
            },
            {
                'title': 'Ultimate Kashmir Adventure',
                'category': 'adventure',
                'destination': destinations['Gulmarg'],
                'duration': '5 Days / 4 Nights',
                'price': 28000,
                'overview': 'For the thrill-seekers! Experience the adrenaline rush of skiing in Gulmarg, trekking in Sonamarg, and rafting in Pahalgam. This package is designed for adventure enthusiasts.',
                'itinerary': '''Day 1: Arrival & Transfer to Gulmarg
Arrival at Srinagar and direct transfer to Gulmarg. Check-in to your hotel. Gear up for your adventure. Evening briefing by our expert guide. Overnight in Gulmarg.

Day 2: Skiing & Snowboarding in Gulmarg
Full day dedicated to snow sports. Take the Gondola to Phase 2 (Apharwat Peak) for advanced skiing or stick to Phase 1 for beginners. Professional instructors available. Evening bonfire at the hotel.

Day 3: Gulmarg to Sonamarg - The Glacier Trek
Drive to Sonamarg. Embark on a trek to the Thajiwas Glacier. Experience the thrill of sledging on snow. Optional: White water rafting in the Sindh river (seasonal). Overnight camping or hotel stay in Sonamarg.

Day 4: Sonamarg to Srinagar via Manasbal
Drive back to Srinagar. En route visit Manasbal Lake (deepest lake in India). Evening free for leisure or shopping. Overnight in Srinagar.

Day 5: Departure
Transfer to airport for your onward journey.''',
                'inclusions': '✅ Accommodation in Hotels/Camps\n✅ Breakfast & Dinner\n✅ Transport by SUV\n✅ Ski Equipment Rental (Basic)\n✅ Guide Charges',
                'exclusions': '❌ Flights\n❌ Gondola Tickets\n❌ Rafting Charges\n❌ Personal Gear (Jackets, Gloves)\n❌ Lunch',
                'is_featured': True,
                'activities': 'skiing, trekking, rafting, camping, adventure',
                'difficulty_level': 'difficult',
                'group_size_min': 4,
                'group_size_max': 12,
                'popularity_score': 88
            },
            {
                'title': 'Kashmir Family Delight',
                'category': 'family',
                'destination': destinations['Pahalgam'],
                'duration': '7 Days / 6 Nights',
                'price': 45000,
                'overview': 'A perfect getaway for the whole family. Relaxed itinerary covering Srinagar, Gulmarg, and Pahalgam with comfortable stays and activities for all age groups.',
                'itinerary': '''Day 1: Arrival in Srinagar
Pick up from airport and transfer to Houseboat. Relax and enjoy the view. Evening Shikara ride.

Day 2: Srinagar - Gulmarg Day Trip
Day trip to Gulmarg. Enjoy the Gondola ride. Kids can enjoy snow activities. Return to Srinagar.

Day 3: Srinagar - Pahalgam
Transfer to Pahalgam. Check-in to hotel. Visit the deer park and amusement park for kids.

Day 4: Pahalgam Sightseeing
Visit Betaab Valley, Aru Valley and Chandanwari. Enjoy the scenic beauty.

Day 5: Pahalgam to Srinagar
Return to Srinagar. Visit Mughal Gardens.

Day 6: Sonamarg Day Trip
Day trip to Sonamarg. Enjoy the meadows and pony rides. Return to Srinagar.

Day 7: Departure
Drop at airport.''',
                'inclusions': '✅ 3 Star Hotel/Houseboat Stay\n✅ Breakfast & Dinner\n✅ Dedicated Vehicle for Family\n✅ Shikara Ride\n✅ Driver Allowance',
                'exclusions': '❌ Entry Tickets\n❌ Lunch\n❌ Union Cab in Pahalgam/Sonamarg\n❌ Pony Rides',
                'is_featured': False,
                'activities': 'sightseeing, family fun, nature, pony ride',
                'difficulty_level': 'easy',
                'group_size_min': 3,
                'group_size_max': 10,
                'popularity_score': 92
            }
        ]
        
        for data in packages_data:
            Package.objects.update_or_create(
                title=data['title'],
                defaults={
                    'slug': slugify(data['title']),
                    'category': data['category'],
                    'destination': data['destination'],
                    'duration': data['duration'],
                    'price': data['price'],
                    'overview': data['overview'],
                    'itinerary': data['itinerary'],
                    'inclusions': data['inclusions'],
                    'exclusions': data['exclusions'],
                    'is_featured': data['is_featured'],
                    'activities': data['activities'],
                    'difficulty_level': data['difficulty_level'],
                    'group_size_min': data['group_size_min'],
                    'group_size_max': data['group_size_max'],
                    'popularity_score': data['popularity_score']
                }
            )
            
        self.stdout.write(self.style.SUCCESS('Successfully populated database'))
