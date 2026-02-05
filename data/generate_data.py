"""
Hajj Nusuk Dashboard - Mock Data Generator
Generates ~200K rows simulating the Hajj 2025 season card management pipeline.
Run once: python data/generate_data.py
"""

import os
import random
import string
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# ── Configuration ──────────────────────────────────────────────────────────
TOTAL_RECORDS = 200_000
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "hajj_data.csv")
SEED = 42

random.seed(SEED)
np.random.seed(SEED)

# ── Person Type Distribution ───────────────────────────────────────────────
PERSON_TYPES = {
    "pilgrim_external": 150_000,
    "pilgrim_internal": 20_000,
    "service_worker": 22_000,
    "government": 5_000,
    "healthcare": 3_000,
}

# ── Nationality Weights (external pilgrims) ────────────────────────────────
EXTERNAL_NATIONALITIES = {
    "Indonesia": 0.16, "Pakistan": 0.13, "India": 0.13, "Bangladesh": 0.09,
    "Nigeria": 0.07, "Iran": 0.06, "Algeria": 0.03, "Turkey": 0.03,
    "Egypt": 0.03, "Sudan": 0.02, "Malaysia": 0.02,
    "Morocco": 0.015, "Iraq": 0.015, "Yemen": 0.015, "Jordan": 0.015,
    "Syria": 0.01, "Tunisia": 0.01, "Libya": 0.01, "Somalia": 0.01,
    "Afghanistan": 0.01, "Uzbekistan": 0.008, "Senegal": 0.008,
    "Tanzania": 0.007, "Niger": 0.007, "Mali": 0.006, "Ethiopia": 0.006,
    "Philippines": 0.005, "China": 0.005, "United Kingdom": 0.005,
    "France": 0.005, "USA": 0.005, "Germany": 0.004, "Russia": 0.004,
    "Bosnia": 0.003, "Thailand": 0.003, "Cameroon": 0.003, "Ghana": 0.003,
    "Guinea": 0.003, "Ivory Coast": 0.003, "Kenya": 0.002,
    "Sri Lanka": 0.002, "Myanmar": 0.002, "Tajikistan": 0.002,
}

# ── Culturally Appropriate Name Database ──────────────────────────────────
# Names transliterated to English letters, culturally appropriate for each region.
# Since these are Hajj pilgrims, almost all names are Islamic.

NAME_DATABASE = {
    "saudi": {
        "male_first": [
            "Mohammed", "Abdullah", "Abdulrahman", "Faisal", "Khalid", "Sultan",
            "Turki", "Bandar", "Saud", "Waleed", "Fahad", "Nasser", "Saleh",
            "Hamad", "Saad", "Tariq", "Adel", "Mansour", "Badr", "Nawaf",
            "Abdulaziz", "Mishal", "Majed", "Naif", "Bader", "Thamer",
            "Rakan", "Yazeed", "Zayed", "Talal",
        ],
        "female_first": [
            "Fatimah", "Noura", "Sarah", "Maha", "Abeer", "Huda", "Layla",
            "Amina", "Reem", "Dalal", "Munira", "Hajar", "Asma", "Wafa",
            "Basma", "Lamia", "Ghada", "Hessa", "Lulwa", "Alanoud",
            "Mashael", "Shaikha", "Jawahir", "Atheer", "Deema", "Sultana",
            "Azzah", "Mounira", "Salwa", "Najla",
        ],
        "last": [
            "Al-Ghamdi", "Al-Harbi", "Al-Shehri", "Al-Zahrani", "Al-Qahtani",
            "Al-Dosari", "Al-Otaibi", "Al-Mutairi", "Al-Rashidi", "Al-Shamri",
            "Al-Subaie", "Al-Anazi", "Al-Hajri", "Al-Malki", "Al-Ahmadi",
            "Al-Khaldi", "Al-Yami", "Al-Bishi", "Al-Asmari", "Al-Thubaiti",
            "Al-Sahli", "Al-Tamimi", "Al-Dawsari", "Al-Johani", "Al-Sulami",
            "Al-Balawi", "Al-Enazi", "Al-Hamdan", "Al-Faifi", "Al-Shahrani",
        ],
    },
    "egypt": {
        "male_first": [
            "Mohamed", "Ahmed", "Mahmoud", "Mustafa", "Ibrahim", "Hassan",
            "Hussein", "Youssef", "Karim", "Tarek", "Amr", "Khaled", "Omar",
            "Adel", "Sherif", "Hossam", "Sameh", "Ashraf", "Gamal", "Emad",
            "Ehab", "Wael", "Alaa", "Tamer", "Hatem", "Medhat", "Nabil",
            "Hany", "Samir", "Magdy",
        ],
        "female_first": [
            "Fatma", "Aisha", "Mariam", "Heba", "Dina", "Amira", "Sahar",
            "Samira", "Nesma", "Eman", "Nourhan", "Rania", "Yasmin", "Mai",
            "Soha", "Mona", "Nagwa", "Naglaa", "Sawsan", "Ghada",
            "Abeer", "Hala", "Noha", "Lobna", "Hanaa", "Amal", "Manal",
            "Inaam", "Rehab", "Doaa",
        ],
        "last": [
            "Hassan", "Hussein", "Mohamed", "Ibrahim", "Ali", "Ahmed",
            "Mahmoud", "Mostafa", "Abdel-Fattah", "El-Sayed", "Attia", "Farag",
            "Osman", "Mansour", "Gamal", "Naguib", "Younis", "Ramadan",
            "Shehata", "Soliman", "Abdallah", "Tawfik", "Badawi", "Metwally",
            "Helmy", "Abdel-Nasser", "Fawzy", "Hafez", "Rizk", "Barakat",
        ],
    },
    "pakistan": {
        "male_first": [
            "Mohammad", "Ahmed", "Ali", "Usman", "Hassan", "Bilal", "Imran",
            "Asad", "Tariq", "Saeed", "Rizwan", "Farhan", "Shahid", "Kamran",
            "Zubair", "Junaid", "Irfan", "Adnan", "Salman", "Hamza",
            "Waqas", "Faisal", "Amir", "Waseem", "Nadeem", "Kashif",
            "Naveed", "Zahid", "Arshad", "Sajid",
        ],
        "female_first": [
            "Fatima", "Ayesha", "Khadija", "Zainab", "Mariam", "Sana", "Hina",
            "Nadia", "Bushra", "Saima", "Rabia", "Uzma", "Asma", "Shabana",
            "Parveen", "Nasreen", "Tahira", "Samina", "Rukhsar", "Sadia",
            "Mehwish", "Farah", "Amna", "Iqra", "Sobia", "Nosheen",
            "Rubina", "Shazia", "Anila", "Farzana",
        ],
        "last": [
            "Khan", "Ahmed", "Ali", "Hussain", "Shah", "Malik", "Iqbal",
            "Siddiqui", "Qureshi", "Butt", "Chaudhry", "Sheikh", "Mirza",
            "Abbasi", "Nawaz", "Hashmi", "Bhatti", "Aslam", "Raza", "Javed",
            "Mughal", "Niazi", "Awan", "Gilani", "Bajwa", "Gondal",
            "Afridi", "Khattak", "Yousafzai", "Durrani",
        ],
    },
    "india_muslim": {
        "male_first": [
            "Mohammad", "Ahmed", "Ali", "Usman", "Hassan", "Bilal", "Imran",
            "Asad", "Tariq", "Saeed", "Rizwan", "Farhan", "Shahid", "Kamran",
            "Zubair", "Junaid", "Irfan", "Adnan", "Salman", "Hamza",
            "Arif", "Riyaz", "Shakeel", "Anwar", "Altaf", "Musheer",
            "Sohail", "Tanveer", "Waheed", "Naeem",
        ],
        "female_first": [
            "Fatima", "Ayesha", "Khadija", "Zainab", "Mariam", "Sana", "Hina",
            "Nadia", "Bushra", "Saima", "Rabia", "Uzma", "Asma", "Shabana",
            "Parveen", "Nasreen", "Tahira", "Samina", "Rukhsar", "Sadia",
            "Reshma", "Mumtaz", "Shahnaz", "Ruksana", "Dilshad", "Tabassum",
            "Nargis", "Gulshan", "Yasmeen", "Nafisa",
        ],
        "last": [
            "Khan", "Ahmed", "Sheikh", "Ansari", "Siddiqui", "Qureshi",
            "Pathan", "Shaikh", "Sayyid", "Hashmi", "Mirza", "Rizvi",
            "Farooqui", "Nadvi", "Idrisi", "Baig", "Naqvi", "Momin", "Beg",
            "Kidwai", "Mansoori", "Nomani", "Quadri", "Usmani", "Dehlvi",
            "Lucknowi", "Azmi", "Falahi", "Islahi", "Madani",
        ],
    },
    "bangladesh": {
        "male_first": [
            "Mohammed", "Abdul", "Rahman", "Hasan", "Karim", "Rahim", "Habib",
            "Rashed", "Shahidul", "Aminul", "Saiful", "Nurul", "Mizanur",
            "Fazlul", "Ashraf", "Zahir", "Rafiq", "Mofiz", "Jahangir",
            "Shahadat", "Monir", "Nazrul", "Shafiq", "Delwar", "Mostafiz",
            "Mahbub", "Azizul", "Abul", "Sohel", "Liton",
        ],
        "female_first": [
            "Fatema", "Ayesha", "Sultana", "Khatun", "Akhter", "Hasina",
            "Nasreen", "Rehana", "Razia", "Monira", "Taslima", "Shirin",
            "Dilara", "Farida", "Hosna", "Nurjahan", "Morsheda", "Anjuman",
            "Rahima", "Amena", "Halima", "Asma", "Kulsum", "Rokeya",
            "Sufia", "Jahanara", "Mst. Rabeya", "Salma", "Shahana", "Bilkis",
        ],
        "last": [
            "Rahman", "Islam", "Hossain", "Ahmed", "Uddin", "Miah", "Chowdhury",
            "Alam", "Haque", "Bhuiyan", "Talukdar", "Sarkar", "Khan",
            "Siddique", "Kamal", "Akbar", "Zaman", "Reza", "Kabir", "Hussain",
            "Mondal", "Mollah", "Bepari", "Howlader", "Biswas",
            "Sikder", "Majumder", "Prodhan", "Gazi", "Munshi",
        ],
    },
    "indonesia": {
        "male_first": [
            "Muhammad", "Ahmad", "Abdul", "Ibrahim", "Yusuf", "Ismail",
            "Ridwan", "Hidayat", "Wahyu", "Rizki", "Agus", "Hendra", "Arif",
            "Fajar", "Surya", "Ramadhan", "Dedi", "Bambang", "Eko",
            "Firmansyah", "Budi", "Andi", "Rudi", "Dani", "Iwan",
            "Joko", "Hendri", "Sigit", "Hadi", "Bayu",
        ],
        "female_first": [
            "Siti", "Nur", "Fatimah", "Aisyah", "Dewi", "Sri", "Rina",
            "Wati", "Yuni", "Fitri", "Indah", "Lestari", "Putri", "Intan",
            "Ayu", "Dian", "Nisa", "Ratna", "Eka", "Wulan",
            "Ani", "Tuti", "Sari", "Mega", "Ningsih", "Rahmawati",
            "Sulistyowati", "Yanti", "Umi", "Mulyani",
        ],
        "last": [
            "Siregar", "Harahap", "Nasution", "Lubis", "Prasetyo", "Wijaya",
            "Santoso", "Hidayat", "Saputra", "Nugroho", "Wibowo", "Setiawan",
            "Purnomo", "Suryadi", "Firmansyah", "Hermawan", "Ramadhan",
            "Gunawan", "Kurniawan", "Susanto", "Suharto", "Sutrisno",
            "Wahyudi", "Handoko", "Supriyadi", "Widodo", "Mulyono",
            "Hartono", "Darmawan", "Iskandar",
        ],
    },
    "malaysia": {
        "male_first": [
            "Muhammad", "Ahmad", "Abdullah", "Ismail", "Ibrahim", "Yusuf",
            "Mohd", "Azman", "Hakim", "Farid", "Shahrul", "Azhar", "Rizal",
            "Hafiz", "Zulkifli", "Aiman", "Fikri", "Nabil", "Syafiq", "Haziq",
            "Azmi", "Hamdan", "Rosli", "Zainal", "Kamal", "Razak",
            "Hanafi", "Zainol", "Shukri", "Bakar",
        ],
        "female_first": [
            "Siti", "Nur", "Fatimah", "Aisyah", "Aminah", "Zarina", "Noor",
            "Haslinda", "Rohana", "Faridah", "Noriah", "Zurina", "Salina",
            "Rashidah", "Hamidah", "Sharifah", "Kamariah", "Mazlina",
            "Ramlah", "Habibah", "Norhayati", "Asmah", "Rosnah", "Mariam",
            "Jamilah", "Azizah", "Rokiah", "Normah", "Zalina", "Hasanah",
        ],
        "last": [
            "Abdullah", "Ibrahim", "Ahmad", "Hassan", "Ismail", "Osman",
            "Yusof", "Zainal", "Idris", "Rahman", "Hamid", "Rashid",
            "Ariffin", "Sulaiman", "Jamaluddin", "Kamaruddin", "Baharuddin",
            "Nooruddin", "Shamsuddin", "Mohd", "Mohamad", "Hashim",
            "Othman", "Razali", "Nordin", "Salleh", "Daud", "Yaacob",
            "Talib", "Aziz",
        ],
    },
    "turkey": {
        "male_first": [
            "Mehmet", "Ahmet", "Mustafa", "Ali", "Hasan", "Ibrahim", "Murat",
            "Yusuf", "Osman", "Kemal", "Bayram", "Fatih", "Serkan", "Burak",
            "Emre", "Cengiz", "Selim", "Bulent", "Erhan", "Ozkan",
            "Recep", "Huseyin", "Ismail", "Suleyman", "Ramazan", "Omer",
            "Cemal", "Halil", "Orhan", "Turgut",
        ],
        "female_first": [
            "Fatma", "Ayse", "Emine", "Hatice", "Zeynep", "Elif", "Merve",
            "Betul", "Kubra", "Havva", "Esra", "Tugba", "Nurcan", "Gulsen",
            "Sevgi", "Aysegul", "Ozlem", "Sibel", "Derya", "Sema",
            "Nurten", "Sultan", "Hacer", "Songul", "Gulizar", "Hanife",
            "Fadime", "Rukiye", "Saliha", "Meryem",
        ],
        "last": [
            "Yilmaz", "Kaya", "Demir", "Celik", "Ozturk", "Aydin", "Erdogan",
            "Arslan", "Dogan", "Kilic", "Aslan", "Ozdemir", "Yildiz",
            "Yildirim", "Ozer", "Aksoy", "Polat", "Sahin", "Korkmaz", "Tekin",
            "Coskun", "Bayrak", "Kaplan", "Taskiran", "Bulut", "Gunes",
            "Koc", "Turan", "Sezer", "Unal",
        ],
    },
    "iran": {
        "male_first": [
            "Mohammad", "Ali", "Hossein", "Hassan", "Reza", "Mehdi", "Amir",
            "Javad", "Saeed", "Hamid", "Ahmad", "Mohsen", "Mostafa", "Majid",
            "Ebrahim", "Naser", "Masoud", "Behzad", "Omid", "Karim",
            "Farhad", "Parviz", "Dariush", "Babak", "Siavash", "Nima",
            "Peyman", "Shahram", "Alireza", "Morteza",
        ],
        "female_first": [
            "Fatimeh", "Zahra", "Maryam", "Narges", "Sakineh", "Somayeh",
            "Leila", "Mina", "Parvin", "Akram", "Masoumeh", "Nasrin",
            "Tahmineh", "Elham", "Azam", "Shahin", "Shohreh", "Mahboubeh",
            "Kobra", "Fereshteh", "Halimeh", "Fatemeh", "Sedigheh",
            "Roghayeh", "Marziyeh", "Nahid", "Afsaneh", "Shirin", "Golnar",
            "Faranak",
        ],
        "last": [
            "Mohammadi", "Hosseini", "Rezaei", "Ahmadi", "Hashemi", "Karimi",
            "Mousavi", "Moradi", "Alavi", "Jafari", "Rahimi", "Sadeghi",
            "Bahrami", "Shirazi", "Tehrani", "Esfahani", "Kazemi", "Fallahi",
            "Tabrizi", "Khorasani", "Abbasi", "Gharibzadeh", "Mansouri",
            "Ebrahimi", "Rostami", "Noori", "Zamani", "Omidi", "Tayebi",
            "Heidari",
        ],
    },
    "nigeria_west_africa": {
        "male_first": [
            "Muhammad", "Ibrahim", "Abubakar", "Usman", "Yusuf", "Musa",
            "Suleiman", "Abdullahi", "Shehu", "Idris", "Aliyu", "Aminu",
            "Garba", "Ismail", "Lawal", "Kabiru", "Nasiru", "Bashir",
            "Danladi", "Bello", "Sanusi", "Auwal", "Haruna", "Nuhu",
            "Adamu", "Salisu", "Hamisu", "Rabiu", "Farouk", "Dahiru",
        ],
        "female_first": [
            "Fatima", "Aisha", "Halima", "Zainab", "Maryam", "Hadiza",
            "Bilkisu", "Amina", "Hauwa", "Rabi", "Salamatu", "Sadiya",
            "Nafisa", "Ruqayya", "Jamila", "Sakina", "Ummu", "Lubabatu",
            "Talatu", "Balkisu", "Hajara", "Barira", "Hassana", "Asiya",
            "Asmau", "Khadija", "Habiba", "Laraba", "Safiya", "Dije",
        ],
        "last": [
            "Abubakar", "Ibrahim", "Mohammed", "Bello", "Yusuf", "Suleiman",
            "Musa", "Danladi", "Abdullahi", "Shehu", "Bala", "Adamu", "Garba",
            "Aliyu", "Ismail", "Lawal", "Tanko", "Jibrin", "Saidu", "Umar",
            "Waziri", "Alkali", "Dikko", "Maigari", "Tukur", "Gwandu",
            "Kafanchan", "Kazaure", "Ringim", "Fagge",
        ],
    },
    "north_africa": {
        "male_first": [
            "Mohamed", "Ahmed", "Youcef", "Mustapha", "Karim", "Abdel",
            "Rachid", "Said", "Hamid", "Noureddine", "Boualem", "Djamel",
            "Farid", "Larbi", "Mounir", "Samir", "Sofiane", "Redouane",
            "Abdelkader", "Nadir", "Brahim", "Hicham", "Amine", "Yassine",
            "Mehdi", "Bilal", "Adel", "Mourad", "Tayeb", "Lahcen",
        ],
        "female_first": [
            "Fatima", "Amina", "Khadija", "Meriem", "Aicha", "Yamina",
            "Djamila", "Houria", "Malika", "Zohra", "Samia", "Naima",
            "Farida", "Souad", "Leila", "Hayat", "Karima", "Nadia",
            "Rachida", "Safia", "Latifa", "Ghania", "Hassiba", "Wahiba",
            "Nacera", "Fatiha", "Siham", "Lamia", "Sabrina", "Imane",
        ],
        "last": [
            "Benali", "Brahim", "Boumediene", "Khelif", "Rahmani", "Saidi",
            "Boudiaf", "Belkacem", "Amrani", "Bensalem", "Mebarki", "Hadjadj",
            "Zidane", "Madani", "Guerrouj", "Alaoui", "Bennani", "Berrada",
            "Idrissi", "Tazi", "Fassi", "Hajji", "Lamrani", "Cherkaoui",
            "Mouline", "Kettani", "Benjelloun", "Senhaji", "Filali", "Tahiri",
        ],
    },
    "sudan_somalia": {
        "male_first": [
            "Mohammed", "Ahmed", "Ibrahim", "Hassan", "Ali", "Osman",
            "Abdullah", "Adam", "Musa", "Hamid", "Abdalla", "Mahgoub",
            "Bashir", "Babiker", "Khalil", "Salih", "Yousif", "Ismail",
            "Abdi", "Nur", "Abdirashid", "Abdikarim", "Dahir", "Guled",
            "Jama", "Farah", "Warsame", "Sharif", "Elyas", "Mahdi",
        ],
        "female_first": [
            "Fatima", "Aisha", "Maryam", "Amina", "Khadija", "Hawa", "Suad",
            "Zeinab", "Samia", "Nawal", "Asma", "Halima", "Fawzia", "Ihsan",
            "Nagla", "Rasha", "Nadia", "Safiya", "Habiba", "Amaal",
            "Hodan", "Ayan", "Sahra", "Nimco", "Fardowsa", "Ubah",
            "Salma", "Zahara", "Marwa", "Bushra",
        ],
        "last": [
            "Ahmed", "Mohammed", "Ibrahim", "Hassan", "Ali", "Osman",
            "Abdullah", "Adam", "Musa", "Hamid", "Abdalla", "Bashir",
            "Babiker", "Khalil", "Salih", "Yousif", "Mahgoub", "Dafalla",
            "Elhaj", "Elsheikh", "Abdi", "Mohamud", "Aden", "Warsame",
            "Hersi", "Yusuf", "Omar", "Farah", "Egal", "Elmi",
        ],
    },
    "levant": {
        "male_first": [
            "Mohammed", "Ahmad", "Ali", "Omar", "Khalil", "Nasser", "Yousef",
            "Samir", "Bassam", "Mazen", "Fadi", "Rami", "Ziad", "Walid",
            "Hani", "Ghassan", "Samer", "Bilal", "Anas", "Hamzah",
            "Marwan", "Khaldoun", "Adnan", "Nizar", "Munir", "Raed",
            "Luay", "Amjad", "Haytham", "Qasim",
        ],
        "female_first": [
            "Fatima", "Aisha", "Maryam", "Huda", "Amina", "Reem", "Layla",
            "Nour", "Dina", "Safa", "Rana", "Lina", "Ghada", "Wafa", "Suha",
            "Haneen", "Rawan", "Abeer", "Sawsan", "Nisreen",
            "Manal", "Taghreed", "Maysoun", "Rula", "Nawal", "Sahar",
            "Lubna", "Hana", "Iman", "Shireen",
        ],
        "last": [
            "Al-Masri", "Al-Khatib", "Al-Husseini", "Al-Khalidi", "Haddad",
            "Nassar", "Sabbagh", "Darwish", "Qasim", "Hamdan", "Salim",
            "Barghouti", "Tamimi", "Nabulsi", "Turk", "Awad", "Jabari",
            "Natsheh", "Amr", "Saadeh", "Khoury", "Bishara", "Mansour",
            "Hourani", "Bakri", "Rantisi", "Dajani", "Asfour", "Mughrabi",
            "Zaatari",
        ],
    },
    "central_asia": {
        "male_first": [
            "Muhammad", "Ahmad", "Abdul", "Rashid", "Karim", "Farid", "Nasir",
            "Hamid", "Jamil", "Habib", "Akbar", "Ismail", "Umar", "Yusuf",
            "Sher", "Noor", "Jawad", "Zaki", "Daud", "Mirwais",
            "Firdaws", "Rustam", "Jamshed", "Behruz", "Khurshed",
            "Dilshod", "Anvar", "Murod", "Sherzod", "Bakhtiar",
        ],
        "female_first": [
            "Fatima", "Maryam", "Zainab", "Nasiba", "Dilraba", "Shirin",
            "Gulnara", "Mahbuba", "Zarrina", "Sitora", "Parvina", "Malika",
            "Zuhra", "Jamila", "Halima", "Anisa", "Rahima", "Latifa",
            "Munira", "Nazira", "Farzona", "Madina", "Nigina", "Sadokat",
            "Tahmina", "Barno", "Mohira", "Shahnoza", "Zulfiya", "Nodira",
        ],
        "last": [
            "Rahimi", "Karimi", "Ahmadzai", "Noori", "Sultani", "Wardak",
            "Ghani", "Fahimi", "Samimi", "Qadiri", "Hasani", "Amiri",
            "Mohammadi", "Hosseini", "Nazari", "Sharifi", "Jafari", "Rezayi",
            "Akbari", "Tahiri", "Rasulov", "Mirzoev", "Karimov", "Rahmonov",
            "Sharipov", "Kholov", "Saidov", "Nematov", "Tursunov", "Boboev",
        ],
    },
    "convert_other": {
        "male_first": [
            "Omar", "Ibrahim", "Yusuf", "Hamza", "Adam", "Zakariya", "Idris",
            "Sulaiman", "Bilal", "Ismail", "Musa", "Nuh", "Dawud", "Haroon",
            "Ayyub", "Mikail", "Khalid", "Mustafa", "Tariq", "Rashid",
            "Zakaria", "Ilyas", "Yahya", "Luqman", "Salahuddin", "Abdur-Rahman",
            "Uthman", "Saifullah", "Jamal", "Kareem",
        ],
        "female_first": [
            "Fatima", "Maryam", "Aisha", "Khadija", "Sarah", "Amina", "Zahra",
            "Safiya", "Huda", "Layla", "Nadia", "Salma", "Yasmin", "Halima",
            "Samira", "Nour", "Rabia", "Sumaya", "Jamilah", "Zainab",
            "Ruqayyah", "Asiya", "Hajar", "Lubna", "Naima", "Sakina",
            "Wardah", "Tasneem", "Bilqis", "Sawda",
        ],
        "last": [
            "Ali", "Hassan", "Ibrahim", "Khan", "Ahmed", "Omar", "Muhammad",
            "Yusuf", "Rahman", "Karim", "Mustafa", "Hamid", "Rashid", "Khalid",
            "Malik", "Noor", "Siddiq", "Amin", "Sharif", "Hasan",
            "Abdullah", "Saleh", "Hussain", "Ismail", "Bakr", "Bilal",
            "Dawoud", "Haroun", "Idris", "Sulaiman",
        ],
    },
}

# ── Nationality to Region Mapping ─────────────────────────────────────────
_NATIONALITY_REGION_MAP = {
    "Saudi Arabia": "saudi",
    "Egypt": "egypt",
    "Pakistan": "pakistan",
    "India": "india_muslim",
    "Bangladesh": "bangladesh",
    "Indonesia": "indonesia",
    "Malaysia": "malaysia",
    "Turkey": "turkey",
    "Iran": "iran",
    "Nigeria": "nigeria_west_africa",
    "Senegal": "nigeria_west_africa",
    "Mali": "nigeria_west_africa",
    "Niger": "nigeria_west_africa",
    "Ghana": "nigeria_west_africa",
    "Guinea": "nigeria_west_africa",
    "Cameroon": "nigeria_west_africa",
    "Ivory Coast": "nigeria_west_africa",
    "Tanzania": "nigeria_west_africa",
    "Kenya": "nigeria_west_africa",
    "Ethiopia": "nigeria_west_africa",
    "Algeria": "north_africa",
    "Morocco": "north_africa",
    "Tunisia": "north_africa",
    "Libya": "north_africa",
    "Sudan": "sudan_somalia",
    "Somalia": "sudan_somalia",
    "Iraq": "levant",
    "Yemen": "levant",
    "Jordan": "levant",
    "Syria": "levant",
    "Afghanistan": "central_asia",
    "Uzbekistan": "central_asia",
    "Tajikistan": "central_asia",
    "Philippines": "indonesia",       # SE Asian Muslims share similar naming
    "China": "convert_other",         # Chinese Muslims (Hui) using transliterated names
    "United Kingdom": "convert_other",
    "France": "convert_other",
    "USA": "convert_other",
    "Germany": "convert_other",
    "Russia": "convert_other",
    "Bosnia": "convert_other",
    "Thailand": "indonesia",          # Thai Muslims share SE Asian naming
    "Sri Lanka": "india_muslim",      # Sri Lankan Muslims share South Asian naming
    "Myanmar": "india_muslim",        # Rohingya share South Asian naming
}


def _get_nationality_region(nationality):
    """Map nationality to a region key in NAME_DATABASE."""
    return _NATIONALITY_REGION_MAP.get(nationality, "convert_other")


def _generate_name(nationality, sex):
    """Generate a culturally appropriate name for the given nationality and sex."""
    region = _get_nationality_region(nationality)
    name_data = NAME_DATABASE[region]

    if sex == "M":
        first_name = random.choice(name_data["male_first"])
    else:
        first_name = random.choice(name_data["female_first"])

    last_name = random.choice(name_data["last"])
    return first_name, last_name

# ── Service Providers (60 fictional companies) ─────────────────────────────
SERVICE_PROVIDERS = [
    f"{'Al' if i % 3 == 0 else 'Dar' if i % 3 == 1 else 'Makkah'} "
    f"{'Safwa' if i % 5 == 0 else 'Tawfiq' if i % 5 == 1 else 'Rahma' if i % 5 == 2 else 'Noor' if i % 5 == 3 else 'Baraka'} "
    f"{'Services' if i % 4 == 0 else 'Group' if i % 4 == 1 else 'Travel' if i % 4 == 2 else 'Hajj Co.'}"
    for i in range(60)
]

# ── Hajj 2025 Timeline ────────────────────────────────────────────────────
SEASON_START = datetime(2025, 4, 1)
SEASON_END = datetime(2025, 6, 30)
ARRIVAL_PEAK = datetime(2025, 5, 18)
ARAFAH_DAY = datetime(2025, 6, 5)
HAJJ_END = datetime(2025, 6, 9)

# Arrival ports with weights
ARRIVAL_PORTS = {
    "Jeddah - KAIA": 0.60,
    "Madinah - Prince Mohammad": 0.25,
    "Makkah - Land Port": 0.10,
    "Yanbu - Sea Port": 0.03,
    "Jeddah - Sea Port": 0.02,
}

ACCOMMODATION_ZONES = [
    "Al Aziziyah", "Al Misfalah", "Al Shisha", "Jarwal", "Al Utaibiyyah",
    "Al Hindawiyyah", "Al Zahra", "Kudai", "Al Rusayfah", "Al Naseem",
    "Mina Camp A", "Mina Camp B", "Mina Camp C", "Arafat Zone 1",
    "Arafat Zone 2", "Muzdalifah Zone",
]


def _s_curve(x, midpoint=0.5, steepness=10):
    """Logistic S-curve for realistic date distribution."""
    return 1 / (1 + np.exp(-steepness * (x - midpoint)))


def _generate_date_in_range(start, end, progress_curve="linear", n=1):
    """Generate dates within a range using different distribution curves."""
    total_days = (end - start).days
    if progress_curve == "s_curve":
        u = np.random.random(n)
        # Inverse S-curve to cluster dates around the middle
        days = (total_days * u).astype(int)
    elif progress_curve == "early_heavy":
        days = np.random.beta(2, 5, n) * total_days
        days = days.astype(int)
    elif progress_curve == "late_heavy":
        days = np.random.beta(5, 2, n) * total_days
        days = days.astype(int)
    else:  # linear / uniform
        days = np.random.randint(0, total_days + 1, n)

    days = np.clip(days, 0, total_days)
    return [start + timedelta(days=int(d)) for d in days]


def generate_persons():
    """Generate person records with types and demographics."""
    print("Generating person records...")

    records = []
    person_id = 1

    for ptype, count in PERSON_TYPES.items():
        print(f"  {ptype}: {count:,} records")

        for i in range(count):
            # ── Nationality ────────────────────────────────────────────
            if ptype == "pilgrim_external":
                nats = list(EXTERNAL_NATIONALITIES.keys())
                weights = list(EXTERNAL_NATIONALITIES.values())
                # Normalize weights
                total_w = sum(weights)
                weights = [w / total_w for w in weights]
                nationality = random.choices(nats, weights=weights, k=1)[0]
            elif ptype == "pilgrim_internal":
                nationality = "Saudi Arabia"
            else:
                # Workers/govt/healthcare: 70% Saudi, 30% mixed
                if random.random() < 0.70:
                    nationality = "Saudi Arabia"
                else:
                    nationality = random.choice([
                        "Egypt", "Pakistan", "India", "Bangladesh",
                        "Philippines", "Indonesia", "Sudan", "Yemen"
                    ])

            # ── Sex ────────────────────────────────────────────────────
            sex = "M" if random.random() < 0.52 else "F"

            # ── Name Generation (culturally appropriate, English letters) ─
            first_name, last_name = _generate_name(nationality, sex)

            # ── Age ────────────────────────────────────────────────────
            if ptype in ("pilgrim_external", "pilgrim_internal"):
                age = int(np.clip(np.random.normal(50, 12), 18, 90))
            elif ptype == "service_worker":
                age = int(np.clip(np.random.normal(30, 7), 20, 55))
            elif ptype == "healthcare":
                age = int(np.clip(np.random.normal(35, 8), 24, 60))
            else:  # government
                age = int(np.clip(np.random.normal(40, 8), 25, 62))

            # ── IDs ────────────────────────────────────────────────────
            if nationality == "Saudi Arabia":
                id_number = f"1{''.join(random.choices(string.digits, k=9))}"
                passport_number = None
            else:
                id_number = f"2{''.join(random.choices(string.digits, k=9))}"
                passport_number = (
                    random.choice(string.ascii_uppercase)
                    + "".join(random.choices(string.digits, k=8))
                )

            # ── B2B / B2C ─────────────────────────────────────────────
            if ptype == "pilgrim_external":
                b2b_b2c = "B2B" if random.random() < 0.85 else "B2C"
            elif ptype == "pilgrim_internal":
                b2b_b2c = "B2B" if random.random() < 0.40 else "B2C"
            else:
                b2b_b2c = "B2B"

            records.append({
                "person_id": person_id,
                "person_type": ptype,
                "first_name": first_name,
                "last_name": last_name,
                "nationality": nationality,
                "age": age,
                "sex": sex,
                "id_number": id_number,
                "passport_number": passport_number,
                "b2b_b2c": b2b_b2c,
            })
            person_id += 1

    return pd.DataFrame(records)


def assign_groups_and_providers(df):
    """Assign service providers and groups."""
    print("Assigning groups and providers...")

    df["service_provider"] = None
    df["group_id"] = None

    group_counter = 1

    for ptype in df["person_type"].unique():
        mask = df["person_type"] == ptype
        indices = df[mask].index.tolist()
        random.shuffle(indices)

        if ptype in ("pilgrim_external", "pilgrim_internal"):
            # Assign to providers
            providers = random.choices(SERVICE_PROVIDERS, k=len(indices))
            df.loc[indices, "service_provider"] = providers

            # Group into batches of 200-500
            i = 0
            while i < len(indices):
                group_size = random.randint(200, 500)
                group_indices = indices[i:i + group_size]
                df.loc[group_indices, "group_id"] = group_counter
                group_counter += 1
                i += group_size

        elif ptype == "service_worker":
            providers = random.choices(SERVICE_PROVIDERS, k=len(indices))
            df.loc[indices, "service_provider"] = providers
            df.loc[indices, "group_id"] = 0  # Workers don't form pilgrim groups

        else:
            df.loc[indices, "service_provider"] = "Government"
            df.loc[indices, "group_id"] = 0

    return df


def assign_family_links(df):
    """Assign spouse_id and father_id links."""
    print("Assigning family links...")

    df["spouse_id"] = None
    df["father_id"] = None

    pilgrim_mask = df["person_type"].isin(["pilgrim_external", "pilgrim_internal"])
    pilgrim_ids = df[pilgrim_mask]["person_id"].tolist()

    # ~25% of pilgrims have spouses (pair them up)
    num_couples = int(len(pilgrim_ids) * 0.125)  # 12.5% * 2 = 25% linked
    random.shuffle(pilgrim_ids)

    for i in range(0, num_couples * 2, 2):
        if i + 1 < len(pilgrim_ids):
            id_a, id_b = pilgrim_ids[i], pilgrim_ids[i + 1]
            df.loc[df["person_id"] == id_a, "spouse_id"] = id_b
            df.loc[df["person_id"] == id_b, "spouse_id"] = id_a

    # ~5% have father links
    remaining = pilgrim_ids[num_couples * 2:]
    num_parent_child = int(len(remaining) * 0.05)
    for i in range(0, num_parent_child * 2, 2):
        if i + 1 < len(remaining):
            df.loc[df["person_id"] == remaining[i + 1], "father_id"] = remaining[i]

    return df


def generate_travel_info(df):
    """Generate travel details: mode, flight, departure country, dates."""
    print("Generating travel info...")

    n = len(df)

    # Travel mode
    travel_modes = np.random.choice(
        ["air", "land", "sea"],
        size=n,
        p=[0.95, 0.045, 0.005]
    )
    df["travel_mode"] = travel_modes

    # Internal pilgrims more likely land
    internal_mask = df["person_type"] == "pilgrim_internal"
    internal_indices = df[internal_mask].index
    df.loc[internal_indices, "travel_mode"] = np.random.choice(
        ["air", "land", "sea"],
        size=len(internal_indices),
        p=[0.30, 0.69, 0.01]
    )

    # Flight number (only for air travelers)
    df["flight_number"] = None
    air_mask = df["travel_mode"] == "air"
    airlines = ["SV", "EK", "QR", "TK", "EY", "GF", "MS", "PK", "GA", "WY"]
    n_air = air_mask.sum()
    df.loc[air_mask, "flight_number"] = [
        f"{random.choice(airlines)}{random.randint(100, 999)}"
        for _ in range(n_air)
    ]

    # Departure country = nationality (for external), Saudi Arabia for internal
    df["departure_country"] = df["nationality"]

    # Arrival port
    ports = list(ARRIVAL_PORTS.keys())
    port_weights = list(ARRIVAL_PORTS.values())

    # Land travelers go through land port
    df["arrival_port"] = np.random.choice(ports, size=n, p=port_weights)
    land_mask = df["travel_mode"] == "land"
    df.loc[land_mask, "arrival_port"] = "Makkah - Land Port"
    sea_mask = df["travel_mode"] == "sea"
    df.loc[sea_mask, "arrival_port"] = np.random.choice(
        ["Yanbu - Sea Port", "Jeddah - Sea Port"],
        size=sea_mask.sum(), p=[0.6, 0.4]
    )

    # Accommodation zone
    df["accommodation_zone"] = np.random.choice(ACCOMMODATION_ZONES, size=n)

    return df


def generate_lifecycle_dates(df):
    """
    Generate the full lifecycle date chain for each record.
    Each stage has a probability of completion and cascading dates.

    Chain: visa -> group_formation -> travel -> arrival ->
           card_printed -> card_at_center -> card_at_provider ->
           card_received -> card_activated -> proof_picture
    """
    print("Generating lifecycle dates (this takes a moment)...")

    n = len(df)

    # ── Visa Issuance ──────────────────────────────────────────────────
    # All external pilgrims get visas (Apr 1 - May 15)
    visa_dates = _generate_date_in_range(
        datetime(2025, 4, 1), datetime(2025, 5, 15), "early_heavy", n
    )
    df["visa_issue_date"] = visa_dates
    df["visa_number"] = [
        f"HJ25{''.join(random.choices(string.digits, k=8))}"
        for _ in range(n)
    ]

    # Internal pilgrims get permits (tasreeh) instead
    internal_mask = df["person_type"] == "pilgrim_internal"
    df.loc[internal_mask, "visa_issue_date"] = _generate_date_in_range(
        datetime(2025, 4, 15), datetime(2025, 5, 25),
        "early_heavy", internal_mask.sum()
    )

    # Workers/govt/healthcare get earlier dates
    staff_mask = df["person_type"].isin(["service_worker", "government", "healthcare"])
    df.loc[staff_mask, "visa_issue_date"] = _generate_date_in_range(
        datetime(2025, 3, 15), datetime(2025, 4, 30),
        "early_heavy", staff_mask.sum()
    )

    # ── Nusuk Number ───────────────────────────────────────────────────
    df["nusuk_number"] = [
        f"NSK-25-{''.join(random.choices(string.digits, k=7))}"
        for _ in range(n)
    ]

    # ── Group Formation ────────────────────────────────────────────────
    # ~96% of groups formed by season
    pilgrim_mask = df["person_type"].isin(["pilgrim_external", "pilgrim_internal"])
    df["group_formation_date"] = None

    pilgrim_indices = df[pilgrim_mask].index
    formed_mask = np.random.random(len(pilgrim_indices)) < 0.96
    formed_indices = pilgrim_indices[formed_mask]

    df.loc[formed_indices, "group_formation_date"] = _generate_date_in_range(
        datetime(2025, 4, 5), datetime(2025, 5, 25), "early_heavy", len(formed_indices)
    )
    # Ensure group formation >= visa date
    for idx in formed_indices:
        visa_d = df.at[idx, "visa_issue_date"]
        group_d = df.at[idx, "group_formation_date"]
        if group_d and visa_d and group_d < visa_d:
            df.at[idx, "group_formation_date"] = visa_d + timedelta(days=random.randint(1, 10))

    # ── Travel & Arrival ───────────────────────────────────────────────
    # S-curve arrivals peaking mid-May
    df["travel_date"] = None
    df["arrival_status"] = False
    df["arrival_date"] = None

    # External pilgrims: arrival window May 1-31
    ext_mask = df["person_type"] == "pilgrim_external"
    ext_indices = df[ext_mask].index
    n_ext = len(ext_indices)

    # Generate S-curve arrival pattern
    arrival_progress = np.random.beta(3, 2.5, n_ext)  # Peaks in middle-late
    total_arrival_days = 31  # May 1-31
    arrival_days = (arrival_progress * total_arrival_days).astype(int)
    arrival_dates_ext = [datetime(2025, 5, 1) + timedelta(days=int(d)) for d in arrival_days]

    # Not all arrive (~93% by season end)
    arrived_ext = np.random.random(n_ext) < 0.93

    for i, idx in enumerate(ext_indices):
        if arrived_ext[i]:
            arr_date = arrival_dates_ext[i]
            df.at[idx, "arrival_date"] = arr_date
            df.at[idx, "arrival_status"] = True
            df.at[idx, "travel_date"] = arr_date - timedelta(days=random.randint(0, 2))

    # Internal pilgrims: arrive May 15 - Jun 3
    int_indices = df[internal_mask].index
    n_int = len(int_indices)
    arrived_int = np.random.random(n_int) < 0.97
    int_arrival_days = np.random.beta(4, 2, n_int) * 19  # 19 days window

    for i, idx in enumerate(int_indices):
        if arrived_int[i]:
            arr_date = datetime(2025, 5, 15) + timedelta(days=int(int_arrival_days[i]))
            df.at[idx, "arrival_date"] = arr_date
            df.at[idx, "arrival_status"] = True
            df.at[idx, "travel_date"] = arr_date - timedelta(days=random.randint(0, 1))

    # Staff: arrive earlier (Apr 15 - May 15)
    staff_indices = df[staff_mask].index
    n_staff = len(staff_indices)
    staff_arrival = np.random.beta(2, 3, n_staff) * 30

    for i, idx in enumerate(staff_indices):
        arr_date = datetime(2025, 4, 15) + timedelta(days=int(staff_arrival[i]))
        df.at[idx, "arrival_date"] = arr_date
        df.at[idx, "arrival_status"] = True
        df.at[idx, "travel_date"] = arr_date - timedelta(days=random.randint(0, 2))

    # ── Card Pipeline (the key metrics) ────────────────────────────────
    print("  Generating card pipeline dates...")

    # Card printed: Apr 15 - May 25, ~75% completion
    df["card_printed"] = False
    df["card_printed_date"] = None

    # Card at center: follows printing by 1-5 days
    df["card_at_center"] = False
    df["card_at_center_date"] = None

    # Card at provider: follows center by 2-7 days
    df["card_at_provider"] = False
    df["card_at_provider_date"] = None

    # Card received: follows provider by 1-5 days
    df["card_received"] = False
    df["card_received_date"] = None

    # Card activated: follows received by 0-7 days
    df["card_activated"] = False
    df["card_activation_date"] = None

    # Proof picture: follows activation by 0-3 days
    df["proof_picture_received"] = False
    df["proof_picture_date"] = None

    # Pipeline probabilities (each stage conditional on previous)
    # These create the realistic funnel drop-off
    pipeline_probs = {
        "pilgrim_external": {
            "printed": 0.72, "center": 0.94, "provider": 0.93,
            "received": 0.88, "activated": 0.59, "proof": 0.85,
        },
        "pilgrim_internal": {
            "printed": 0.55, "center": 0.90, "provider": 0.90,
            "received": 0.85, "activated": 0.50, "proof": 0.80,
        },
        "service_worker": {
            "printed": 0.65, "center": 0.90, "provider": 0.88,
            "received": 0.80, "activated": 0.55, "proof": 0.75,
        },
        "government": {
            "printed": 0.80, "center": 0.95, "provider": 0.95,
            "received": 0.95, "activated": 0.90, "proof": 0.90,
        },
        "healthcare": {
            "printed": 0.80, "center": 0.95, "provider": 0.95,
            "received": 0.95, "activated": 0.90, "proof": 0.90,
        },
    }

    for ptype, probs in pipeline_probs.items():
        type_mask = df["person_type"] == ptype
        type_indices = df[type_mask].index
        n_type = len(type_indices)

        # Card printed
        printed_roll = np.random.random(n_type)
        printed_mask = printed_roll < probs["printed"]
        printed_indices = type_indices[printed_mask]

        print_dates = _generate_date_in_range(
            datetime(2025, 4, 15), datetime(2025, 5, 25),
            "early_heavy", len(printed_indices)
        )
        df.loc[printed_indices, "card_printed"] = True
        df.loc[printed_indices, "card_printed_date"] = print_dates

        # Card at center (conditional on printed)
        center_roll = np.random.random(len(printed_indices))
        center_mask = center_roll < probs["center"]
        center_indices = printed_indices[center_mask]

        for idx in center_indices:
            print_d = df.at[idx, "card_printed_date"]
            if print_d:
                df.at[idx, "card_at_center"] = True
                df.at[idx, "card_at_center_date"] = print_d + timedelta(
                    days=random.randint(1, 5)
                )

        # Card at provider (conditional on at center)
        provider_roll = np.random.random(len(center_indices))
        provider_mask = provider_roll < probs["provider"]
        provider_indices = center_indices[provider_mask]

        for idx in provider_indices:
            center_d = df.at[idx, "card_at_center_date"]
            if center_d:
                df.at[idx, "card_at_provider"] = True
                df.at[idx, "card_at_provider_date"] = center_d + timedelta(
                    days=random.randint(2, 7)
                )

        # Card received (conditional on at provider AND person arrived)
        received_roll = np.random.random(len(provider_indices))
        received_mask = received_roll < probs["received"]
        received_indices = provider_indices[received_mask]

        for idx in received_indices:
            provider_d = df.at[idx, "card_at_provider_date"]
            arrival_d = df.at[idx, "arrival_date"]
            if provider_d:
                base_date = provider_d
                if arrival_d and arrival_d > provider_d:
                    base_date = arrival_d
                df.at[idx, "card_received"] = True
                df.at[idx, "card_received_date"] = base_date + timedelta(
                    days=random.randint(1, 5)
                )

        # Card activated (conditional on received)
        activated_roll = np.random.random(len(received_indices))
        activated_mask = activated_roll < probs["activated"]
        activated_indices = received_indices[activated_mask]

        for idx in activated_indices:
            received_d = df.at[idx, "card_received_date"]
            if received_d:
                df.at[idx, "card_activated"] = True
                df.at[idx, "card_activation_date"] = received_d + timedelta(
                    days=random.randint(0, 7)
                )

        # Proof picture (conditional on activated)
        proof_roll = np.random.random(len(activated_indices))
        proof_mask = proof_roll < probs["proof"]
        proof_indices = activated_indices[proof_mask]

        for idx in proof_indices:
            act_d = df.at[idx, "card_activation_date"]
            if act_d:
                df.at[idx, "proof_picture_received"] = True
                df.at[idx, "proof_picture_date"] = act_d + timedelta(
                    days=random.randint(0, 3)
                )

    return df


def generate_health_data(df):
    """Generate health incidents and death records."""
    print("Generating health data...")

    n = len(df)

    df["health_status"] = "none"
    df["health_date"] = None
    df["health_notes"] = None
    df["death_status"] = False
    df["death_date"] = None

    # Health incident risk varies by person type and age
    health_roll = np.random.random(n)

    # External pilgrims: higher risk (base 2.5%, 7% for 65+, 4% for 55+)
    # Internal pilgrims (mostly Saudi): lower risk (base 1%, 3% for 65+, 1.5% for 55+)
    # Workers/govt/healthcare: lowest risk (base 0.5%, no age escalation)
    is_external = df["person_type"] == "pilgrim_external"
    is_internal = df["person_type"] == "pilgrim_internal"
    is_staff = df["person_type"].isin(["service_worker", "government", "healthcare"])

    age_risk = np.full(n, 0.025)  # default (shouldn't be hit)

    # External pilgrims
    age_risk = np.where(
        is_external & (df["age"] >= 65), 0.07,
        np.where(is_external & (df["age"] >= 55), 0.04,
                 np.where(is_external, 0.025, age_risk))
    )
    # Internal pilgrims
    age_risk = np.where(
        is_internal & (df["age"] >= 65), 0.03,
        np.where(is_internal & (df["age"] >= 55), 0.015,
                 np.where(is_internal, 0.01, age_risk))
    )
    # Staff (workers, govt, healthcare)
    age_risk = np.where(is_staff, 0.005, age_risk)

    health_mask = health_roll < age_risk
    health_indices = df[health_mask].index

    severities = np.random.choice(
        ["minor", "moderate", "severe", "critical"],
        size=len(health_indices),
        p=[0.50, 0.30, 0.15, 0.05]
    )
    df.loc[health_indices, "health_status"] = severities

    # Health incidents mostly during Hajj rituals (Jun 4-9) and arrival period
    health_dates = []
    for _ in range(len(health_indices)):
        if random.random() < 0.6:
            # During Hajj rituals
            d = datetime(2025, 6, 4) + timedelta(days=random.randint(0, 5))
        elif random.random() < 0.5:
            # During arrival
            d = datetime(2025, 5, 10) + timedelta(days=random.randint(0, 20))
        else:
            # Random during season
            d = datetime(2025, 4, 15) + timedelta(days=random.randint(0, 70))
        health_dates.append(d)

    df.loc[health_indices, "health_date"] = health_dates

    health_notes_list = [
        "Heat exhaustion", "Dehydration", "Respiratory infection",
        "Cardiac event", "Fracture - fall", "Gastrointestinal illness",
        "Hypertension crisis", "Diabetes complication", "Allergic reaction",
        "Heatstroke", "Pneumonia", "Urinary tract infection",
        "Chronic disease exacerbation", "Skin infection", "Eye infection",
    ]
    df.loc[health_indices, "health_notes"] = np.random.choice(
        health_notes_list, size=len(health_indices)
    )

    # Deaths: ~0.05% overall, higher for critical cases
    critical_mask = df["health_status"] == "critical"
    severe_mask = df["health_status"] == "severe"

    # 30% of critical cases, 5% of severe
    critical_indices = df[critical_mask].index
    severe_indices = df[severe_mask].index

    death_critical = critical_indices[np.random.random(len(critical_indices)) < 0.30]
    death_severe = severe_indices[np.random.random(len(severe_indices)) < 0.05]
    death_indices = death_critical.union(death_severe)

    df.loc[death_indices, "death_status"] = True
    for idx in death_indices:
        health_d = df.at[idx, "health_date"]
        if health_d:
            df.at[idx, "death_date"] = health_d + timedelta(days=random.randint(0, 3))
        else:
            df.at[idx, "death_date"] = datetime(2025, 6, 5) + timedelta(
                days=random.randint(0, 5)
            )

    return df


def main():
    print("=" * 60)
    print("Hajj Nusuk Dashboard - Data Generator")
    print("=" * 60)
    print(f"Generating {TOTAL_RECORDS:,} records...")
    print()

    # Step 1: Generate persons
    df = generate_persons()
    print(f"  Total records: {len(df):,}")

    # Step 2: Assign groups and providers
    df = assign_groups_and_providers(df)

    # Step 3: Family links
    df = assign_family_links(df)

    # Step 4: Travel info
    df = generate_travel_info(df)

    # Step 5: Lifecycle dates
    df = generate_lifecycle_dates(df)

    # Step 6: Health data
    df = generate_health_data(df)

    # ── Save to CSV ────────────────────────────────────────────────────
    print()
    print(f"Saving to {OUTPUT_PATH}...")
    df.to_csv(OUTPUT_PATH, index=False)

    file_size = os.path.getsize(OUTPUT_PATH) / (1024 * 1024)
    print(f"File size: {file_size:.1f} MB")

    # ── Verification ───────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("VERIFICATION")
    print("=" * 60)
    print(f"Total rows: {len(df):,}")
    print()
    print("Person type distribution:")
    print(df["person_type"].value_counts().to_string())
    print()
    print("Top 10 nationalities (external pilgrims):")
    ext = df[df["person_type"] == "pilgrim_external"]
    nat_pct = ext["nationality"].value_counts(normalize=True).head(10) * 100
    print(nat_pct.round(1).to_string())
    print()
    print(f"Male ratio: {(df['sex'] == 'M').mean():.1%}")
    print(f"Mean age (pilgrims): {df[df['person_type'].str.startswith('pilgrim')]['age'].mean():.1f}")
    print()
    print("Card pipeline (all records):")
    print(f"  Printed:    {df['card_printed'].sum():>8,} ({df['card_printed'].mean():.1%})")
    print(f"  At center:  {df['card_at_center'].sum():>8,} ({df['card_at_center'].mean():.1%})")
    print(f"  At provider:{df['card_at_provider'].sum():>8,} ({df['card_at_provider'].mean():.1%})")
    print(f"  Received:   {df['card_received'].sum():>8,} ({df['card_received'].mean():.1%})")
    print(f"  Activated:  {df['card_activated'].sum():>8,} ({df['card_activated'].mean():.1%})")
    print(f"  Proof pic:  {df['proof_picture_received'].sum():>8,} ({df['proof_picture_received'].mean():.1%})")
    print()
    print(f"Arrivals: {df['arrival_status'].sum():,} ({df['arrival_status'].mean():.1%})")
    print(f"Health incidents: {(df['health_status'] != 'none').sum():,}")
    print(f"Deaths: {df['death_status'].sum():,}")
    print()
    print("Done!")


if __name__ == "__main__":
    main()
