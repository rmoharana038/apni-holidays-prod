#!/usr/bin/env python3
"""
Mock data for development when Firestore is not available
This will be replaced with real Firestore in production
"""
from datetime import datetime

# Mock packages data
PACKAGES = [
    {
        'id': 'pkg_thailand_001',
        'title': 'Thailand Explorer: City & Coast Edition',
        'destination': 'Thailand',
        'days': 7,
        'price': 35575.00,
        'discount_price': 31289.00,
        'description': "Experience the best of Thailand with our carefully crafted 7-day package covering Bangkok's vibrant city life and coastal paradise. From temple hopping to beach relaxation, this package offers the perfect blend of culture and leisure.",
        'highlights': "Chao Phraya dinner cruise, Tiger kingdom, Temple visits, Beach activities, Shopping tours",
        'inclusions': "4-star accommodation, Daily breakfast, Airport transfers, Domestic flights, Sightseeing tours, English speaking guide",
        'exclusions': "International flights, Travel insurance, Visa fees, Personal expenses, Tips and gratuities",
        'itinerary': "Day 1: Arrival in Bangkok - Airport transfer to hotel, Evening Chao Phraya dinner cruise\nDay 2: Bangkok city tour - Grand Palace, Wat Pho temple, Local markets\nDay 3: Bangkok to Phuket - Domestic flight, Beach relaxation\nDay 4: Phuket island hopping - Phi Phi island tour with lunch\nDay 5: Tiger Kingdom and adventure activities\nDay 6: Free day for shopping and relaxation\nDay 7: Departure - Transfer to airport",
        'image_url': 'https://i.ibb.co/20fQ1nMQ/cdeeced219a0.jpg',
        'featured': True,
        'status': 'active',
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    },
    {
        'id': 'pkg_dubai_001',
        'title': 'DUBAI 3 NIGHT 04 DAYS',
        'destination': 'Dubai',
        'days': 4,
        'price': 29999.00,
        'discount_price': 19999.00,
        'description': "Discover the glamour and luxury of Dubai in this exciting 4-day package. Experience world-class shopping, stunning architecture, and thrilling desert adventures in the jewel of the Middle East.",
        'highlights': "Burj Khalifa visit, Desert safari, Dubai Mall, Gold Souk, Marina cruise",
        'inclusions': "3-star hotel accommodation, Daily breakfast, Airport transfers, Desert safari with BBQ dinner, Dubai city tour",
        'exclusions': "International flights, Travel insurance, Visa fees, Lunch and dinner (except mentioned), Personal shopping",
        'itinerary': "Day 1: Arrival - Airport transfer, Hotel check-in, Evening at leisure\nDay 2: Dubai city tour - Burj Khalifa, Dubai Mall, Gold Souk\nDay 3: Desert safari with BBQ dinner and entertainment\nDay 4: Departure - Last minute shopping, Transfer to airport",
        'image_url': 'https://i.ibb.co/xq9W5tJ4/7d127688b61c.jpg',
        'featured': True,
        'status': 'active',
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    },
    {
        'id': 'pkg_phuket_001',
        'title': 'Budget Bliss in Phuket',
        'destination': 'Thailand',
        'days': 4,
        'price': 17999.00,
        'discount_price': 12699.00,
        'description': 'Enjoy the beautiful beaches and vibrant nightlife of Phuket without breaking the bank. This budget-friendly package includes the famous Phi Phi Island tour and comfortable accommodation.',
        'highlights': "Phi Phi island tour, Patong Beach, Local markets, Thai massage, Sunset viewing",
        'inclusions': "Budget hotel accommodation, Daily breakfast, Airport transfers, Phi Phi island tour with lunch, Local sightseeing",
        'exclusions': "International flights, Travel insurance, Visa fees, Dinners, Alcoholic beverages, Water sports",
        'itinerary': "Day 1: Arrival in Phuket - Airport transfer, Beach relaxation\nDay 2: Phi Phi island tour with lunch and snorkeling\nDay 3: Phuket city tour and Patong Beach visit\nDay 4: Departure - Transfer to airport",
        'image_url': 'https://i.ibb.co/Ld6jSyPr/775899a0d448.jpg',
        'featured': True,
        'status': 'active',
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    },
    {
        'id': 'pkg_bali_001',
        'title': 'Bali Cultural Discovery',
        'destination': 'Bali',
        'days': 6,
        'price': 42000.00,
        'discount_price': 38000.00,
        'description': "Immerse yourself in the rich culture and natural beauty of Bali. Visit ancient temples, witness traditional arts, and relax on pristine beaches in this comprehensive cultural tour.",
        'highlights': "Tanah Lot temple, Ubud rice terraces, Traditional dance show, Volcano tour, Beach relaxation",
        'inclusions': "4-star resort accommodation, Daily breakfast, All transfers, Temple visits, Cultural performances, English guide",
        'exclusions': "International flights, Travel insurance, Visa fees, Lunches and dinners, Spa treatments, Shopping",
        'itinerary': "Day 1: Arrival - Airport transfer, Welcome dinner\nDay 2: Ubud tour - Rice terraces, Monkey forest, Art villages\nDay 3: Temple tour - Tanah Lot, Uluwatu with Kecak dance\nDay 4: Volcano tour - Mount Batur sunrise trek\nDay 5: Beach day - Sanur or Nusa Dua relaxation\nDay 6: Departure - Last minute shopping, Airport transfer",
        'image_url': 'https://i.ibb.co/placeholder-bali.jpg',
        'featured': False,
        'status': 'active',
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    },
    {
        'id': 'pkg_singapore_001',
        'title': 'Singapore Highlights',
        'destination': 'Singapore',
        'days': 5,
        'price': 49999.00,
        'discount_price': 34999.00,
        'description': "Experience the garden city of Singapore with this comprehensive package covering major attractions, cultural districts, and entertainment venues in this modern metropolis.",
        'highlights': "Gardens by the Bay, Marina Bay Sands, Sentosa Island, Night Safari, Cultural quarters",
        'inclusions': "4-star hotel accommodation, Daily breakfast, All transfers, Attraction tickets, City tour, Night safari",
        'exclusions': "International flights, Travel insurance, Meals (except breakfast), Cable car rides, Shopping, Tips",
        'itinerary': "Day 1: Arrival - Airport transfer, Marina Bay area walk\nDay 2: City tour - Merlion, Chinatown, Little India, Arab Street\nDay 3: Gardens by the Bay and Marina Bay Sands SkyPark\nDay 4: Sentosa Island - Universal Studios or S.E.A. Aquarium\nDay 5: Night Safari, Departure preparation",
        'image_url': 'https://i.ibb.co/placeholder-singapore.jpg',
        'featured': False,
        'status': 'active',
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    }
]

# Mock users data  
USERS = [
    # Admin Users
    {
        'id': 'usr_rajesh_admin',
        'name': 'Rajesh (Admin)',
        'email': 'rajesh4telecom@gmail.com', 
        'phone': '+91-8819881881',
        'password': 'scrypt:32768:8:1$0ykf9ZV7s3P6o0b8$62c6bc22b90ef79a420435141c3c5ace6d1269a3458b9cf8b66896bbb182f6ac58911c952c48dbd63b1b460e46e0a0024be9aa4a1158e547dd481693d708e515',
        'firebase_uid': '',
        'status': 'active',
        'role': 'admin',
        'created_at': datetime.now(),
        'last_login': None
    },
    {
        'id': 'usr_admin_main',
        'name': 'Apni (Admin)',
        'email': 'admin@apniholidays.com',
        'phone': '+91-6371573038',
        'password': 'scrypt:32768:8:1$0ykf9ZV7s3P6o0b8$62c6bc22b90ef79a420435141c3c5ace6d1269a3458b9cf8b66896bbb182f6ac58911c952c48dbd63b1b460e46e0a0024be9aa4a1158e547dd481693d708e515',
        'firebase_uid': '',
        'status': 'active',
        'role': 'admin',
        'created_at': datetime.now(),
        'last_login': None
    },
    {
        'id': 'usr_rkm1_admin',
        'name': 'RKM-1 (Admin)',
        'email': 'rkm.ytw1@gmail.com',
        'phone': '+91-9876543209',
        'password': 'scrypt:32768:8:1$0ykf9ZV7s3P6o0b8$62c6bc22b90ef79a420435141c3c5ace6d1269a3458b9cf8b66896bbb182f6ac58911c952c48dbd63b1b460e46e0a0024be9aa4a1158e547dd481693d708e515',
        'firebase_uid': '',
        'status': 'active',
        'role': 'admin',
        'created_at': datetime.now(),
        'last_login': None
    },
    # Regular Users
    {
        'id': 'usr_rkm2_user',
        'name': 'RKM-2 (User)',
        'email': 'rkm.ytw2@gmail.com',
        'phone': '+91-9876543210',
        'password': 'scrypt:32768:8:1$0ykf9ZV7s3P6o0b8$62c6bc22b90ef79a420435141c3c5ace6d1269a3458b9cf8b66896bbb182f6ac58911c952c48dbd63b1b460e46e0a0024be9aa4a1158e547dd481693d708e515',
        'firebase_uid': '',
        'status': 'active',
        'role': 'user',
        'created_at': datetime.now(),
        'last_login': None
    },
    {
        'id': 'usr_rkm3_user',
        'name': 'RKM-3 (User)',
        'email': 'rkm.ytw3@gmail.com',
        'phone': '+91-9876543211',
        'password': 'scrypt:32768:8:1$0ykf9ZV7s3P6o0b8$62c6bc22b90ef79a420435141c3c5ace6d1269a3458b9cf8b66896bbb182f6ac58911c952c48dbd63b1b460e46e0a0024be9aa4a1158e547dd481693d708e515',
        'firebase_uid': '',
        'status': 'active',
        'role': 'user',
        'created_at': datetime.now(),
        'last_login': None
    },
    {
        'id': 'usr_rkm4_user',  
        'name': 'RKM-4 (User)',
        'email': 'rkm.ytw4@gmail.com',
        'phone': '+91-9876543212',
        'password': 'scrypt:32768:8:1$0ykf9ZV7s3P6o0b8$62c6bc22b90ef79a420435141c3c5ace6d1269a3458b9cf8b66896bbb182f6ac58911c952c48dbd63b1b460e46e0a0024be9aa4a1158e547dd481693d708e515',
        'firebase_uid': '',
        'status': 'active',
        'role': 'user',
        'created_at': datetime.now(),
        'last_login': None
    }
]