"""Sunday April 19, 2026 — FQF schedule data.

DEPRECATED: This file is no longer the authoritative source of schedule data.
The canonical data lives in src/fqf/data/fq2026_acts.yaml.
This file is kept for reference only and is not imported by the package.
"""

from fqf.models import (
    ABITA,
    CAFEBEIGNET,
    DUTCHALLEY,
    ENTERGY,
    FISHFRY,
    FRENCHMARKET,
    HANCOCK,
    HOUSEOFBLUES,
    JACKDANIELS,
    JAZZPARK,
    JAZZPLAYHOUSE,
    KREWE,
    LOYOLA,
    NEWORLEANS,
    OMNI,
    PANAMLIFE,
    SCHOOLHOUSE,
    SUN,
    TROPICAL,
    WILLOW,
    AboutSource,
    Act,
    Genre,
    t,
)

SUNDAY_ACTS: list[Act] = [
    # ── Abita Beer Stage ──────────────────────────────────────────────
    Act(
        "Sam Price & the True Believers",
        ABITA,
        SUN,
        t(11, 30),
        t(12, 30),
        genre=Genre.ROCK,
        about=(
            "Bassist and vocalist Sam Price formed the True Believers in 2015\n"
            "as an outlet for his original songwriting, drawing on decades of\n"
            "experience in the New Orleans music scene since 1992. Best known\n"
            "for his work with the Honey Island Swamp Band and Afro-Cuban jazz\n"
            "group OTRA, Price brings a genre-hopping sensibility to the band's\n"
            "self-described soul-rock and funk-roll sound. Their debut EP was\n"
            "named Best Roots Rock Album of 2017."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[
            "https://sampricemusic.com/",
            "https://sampriceandthetruebelievers.bandcamp.com/",
        ],
    ),
    Act(
        "Bucktown All-Stars",
        ABITA,
        SUN,
        t(12, 50),
        t(13, 50),
        genre=Genre.FUNK,
        about=(
            "Established in 1992, the Bucktown All-Stars are a brass-driven\n"
            "New Orleans party institution fueled by raspy vocals, rollicking\n"
            "piano, and a gloriously corrupt horn section. Their unorthodox mix\n"
            "of second line funk and Motown soul has earned them a multi-year\n"
            "Gambit Reader's Poll win for Best Band That Doesn't Fit Any\n"
            "Category, plus ten Offbeat Best of the Beat Awards. Expect\n"
            "non-stop dancing from start to finish."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.bucktownallstars.com/"],
    ),
    Act(
        "New Orleans Suspects",
        ABITA,
        SUN,
        t(14, 10),
        t(15, 10),
        genre=Genre.FUNK,
        about=(
            "Born in 2009 as a pick-up band at the Maple Leaf Bar, the New\n"
            "Orleans Suspects bring together some of the city's most seasoned\n"
            "players, including Mean Willie Green from the Neville Brothers on\n"
            "drums. Their sound mixes irresistibly tight funk, soulful horns,\n"
            "and Americana-based rhythm and blues with a pinch of jamband\n"
            "groove. Over the years they've built a devout following across\n"
            "the festival and club circuits nationwide."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://neworleanssuspects.com/"],
    ),
    Act(
        "Jelly Joseph",
        ABITA,
        SUN,
        t(15, 30),
        t(16, 30),
        genre=Genre.MIXED_ECLECTIC,
        about=(
            "Grammy-nominated singer-songwriter Anjelika 'Jelly' Joseph is\n"
            "one of the most versatile voices in New Orleans. Raised on her\n"
            "mother's gospel roots and father's soulful blues, she cut her\n"
            "chops on Bourbon Street, appeared on American Idol, and sang\n"
            "backing vocals with Tank and the Bangas before commanding stages\n"
            "worldwide as lead singer of the funk-jazz juggernaut Galactic.\n"
            "She also performs with the Original Pinettes, the city's beloved\n"
            "all-female brass band, and was named JAMNOLA's Music Ambassador."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.wwoz.org/acts/anjelika-jelly-joseph"],
    ),
    Act(
        "Hasizzle with TBC Brass Band",
        ABITA,
        SUN,
        t(17, 0),
        t(18, 20),
        genre=Genre.BRASS_BAND,
        about=(
            "The self-proclaimed King of Bounce meets one of the city's most\n"
            "exciting young brass bands. HaSizzle grew up in the Calliope\n"
            "projects, has been sampled by Drake and Lil Wayne, and brings\n"
            "non-stop booty-shakin' energy to every stage. The To Be Continued\n"
            "Brass Band started on high school grounds and French Quarter\n"
            "street corners before being taken under the wing of The Roots,\n"
            "who produced the 2010 documentary 'From the Mouthpiece on Back'\n"
            "about their journey. Together they deliver a high-voltage collision\n"
            "of bounce and brass."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.wwoz.org/acts/tbc-brass-band"],
    ),
    Act(
        "Cyril Neville",
        ABITA,
        SUN,
        t(18, 50),
        t(20, 0),
        genre=Genre.FUNK,
        about=(
            "One of the founding fathers of New Orleans' signature funky soul\n"
            "sound, Cyril Neville has entertained audiences for over five\n"
            "decades. He first rose to prominence as a member of his brother\n"
            "Art's legendary band the Meters, then co-founded the Neville\n"
            "Brothers, winning a 1989 Grammy for 'Healing Chant.' His resume\n"
            "includes collaborations with Bob Dylan, Robbie Robertson, Dr. John,\n"
            "and Royal Southern Brotherhood. A living link to the deepest roots\n"
            "of New Orleans music."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.cyrilnevillemusic.com/"],
    ),
    # ── NewOrleans.com Stage ──────────────────────────────────────────
    Act(
        "Tuba Skinny",
        NEWORLEANS,
        SUN,
        t(11, 15),
        t(12, 25),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "What started as a loose collection of street musicians busking in\n"
            "the French Quarter has grown into a worldwide phenomenon. Led by\n"
            "cornetist Shaye Cohn, Tuba Skinny plays early jazz, ragtime, and\n"
            "blues of the 1920s and '30s with infectious authenticity. They've\n"
            "released over a dozen albums, toured internationally from Sweden\n"
            "to Australia, and attracted high-profile fans including R. Crumb,\n"
            "Amanda Palmer, and Neil Gaiman. Named after a passerby's joke\n"
            "about tubist Todd Burdick's slender frame."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["http://tubaskinny.com/"],
    ),
    Act(
        "Lena Prima",
        NEWORLEANS,
        SUN,
        t(12, 45),
        t(14, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "The youngest daughter of legendary trumpeter Louis Prima, Lena\n"
            "Prima carries forward a rich musical legacy while forging her own\n"
            "dynamic path. Born in Las Vegas and now based in New Orleans, she\n"
            "held a beloved 14-year residency at the Hotel Monteleone's\n"
            "Carousel Bar. With eight albums, a Billboard Jazz Top Ten release,\n"
            "and a high-energy stage show that channels swing, jazz, and rock,\n"
            "she is a powerhouse vocalist who fills every room she enters."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.lenaprima.com/"],
    ),
    Act(
        "Jeremy Davenport",
        NEWORLEANS,
        SUN,
        t(14, 20),
        t(15, 30),
        genre=Genre.JAZZ_CONTEMPORARY,
        about=(
            "Jazz trumpeter and singer Jeremy Davenport studied under Ellis\n"
            "Marsalis at the University of New Orleans, toured with Harry\n"
            "Connick Jr.'s Big Band for six years, and has shared stages with\n"
            "Sting, Paul McCartney, and Diana Krall. His 25-year residency at\n"
            "the Davenport Lounge at The Ritz-Carlton, New Orleans, is a local\n"
            "institution. His smooth vocal style and polished horn work blend\n"
            "jazz standards with swinging originals."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://jeremydavenport.com/"],
    ),
    Act(
        "Judith Owen & Her Gentlemen Callers",
        NEWORLEANS,
        SUN,
        t(15, 50),
        t(17, 10),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "Welsh singer-songwriter Judith Owen brings a stylistic range that\n"
            "spans rock, pop, jazz, blues, and cabaret. Daughter of opera\n"
            "singer Handel Owen, she grew up surrounded by classical music in\n"
            "London before launching a recording career with thirteen albums\n"
            "to her name. Her 2022 release 'Come On & Get It' pays tribute to\n"
            "female jazz and blues singers of the 1940s and '50s. Married to\n"
            "actor and fellow New Orleans resident Harry Shearer."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://judithowen.net/"],
    ),
    Act(
        "Delfeayo Marsalis & the Uptown Jazz Orchestra",
        NEWORLEANS,
        SUN,
        t(17, 30),
        t(18, 45),
        genre=Genre.JAZZ_CONTEMPORARY,
        about=(
            "NEA Jazz Master and middle Marsalis brother Delfeayo formed the\n"
            "Uptown Jazz Orchestra in 2000 to preserve jazz traditions like\n"
            "New Orleans polyphony, riff playing, and spontaneous arrangements.\n"
            "Leading from his seat in the trombone section, he drives an\n"
            "ensemble that Downbeat described as blending the dance-driven\n"
            "energy of the Dirty Dozen with the sophistication of Basie,\n"
            "Ellington, Mingus, and Coltrane. One of the premier large\n"
            "jazz ensembles in the world."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://theujo.org/", "https://www.dmarsalis.com/"],
    ),
    # ── Tropical Isle Hand Grenade Stage ──────────────────────────────
    Act(
        "Professor Craig Adams & the Higher Dimensions Band",
        TROPICAL,
        SUN,
        t(11, 10),
        t(12, 10),
        genre=Genre.GOSPEL,
        about=(
            "Professor Craig Adams carries on a family gospel tradition with\n"
            "his father Craig Adams Sr.'s Higher Dimensions of Praise Gospel\n"
            "Band, delivering a wide range of gospel styles with a heavy New\n"
            "Orleans accent. The group has performed at Jazz Fest and French\n"
            "Quarter Festival multiple times, uplifting crowds with spirited\n"
            "arrangements rooted in the city's deep church music heritage."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[],
    ),
    Act(
        "Alex McMurray",
        TROPICAL,
        SUN,
        t(12, 30),
        t(13, 30),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "Since arriving from New Jersey as a Tulane student in the 1980s,\n"
            "Alex McMurray has become one of New Orleans' most prolific and\n"
            "respected songwriters. He leads his own band and plays in over a\n"
            "dozen others, including Tin Men and Happy Talk Band. Winner of\n"
            "Big Easy awards for Best Roots Rock Artist and Album of the Year,\n"
            "he's been performing at Jazz Fest since 1993 and played himself\n"
            "on HBO's Treme."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://alexmcmurray.com/"],
    ),
    Act(
        "Assata Renay",
        TROPICAL,
        SUN,
        t(13, 50),
        t(14, 50),
        genre=Genre.RNB_SOUL,
        about=(
            "Raised in New Orleans by a blues-guitarist grandfather and parents\n"
            "who fed her old-school R&B, Assata Renay is a powerhouse vocalist,\n"
            "magnetic performer, and skilled DJ. In 2019, she sang her way to\n"
            "American Idol's Top 40, and in 2023 she starred as Rachel Marron\n"
            "in The Bodyguard at the Anthony Bean Theatre. Whether curating\n"
            "beats for the dance floor or delivering soul-stirring live vocals,\n"
            "she brings passion and precision to every stage."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://assatarenay.com/"],
    ),
    Act(
        "Wanda Rouzan and a Taste of New Orleans",
        TROPICAL,
        SUN,
        t(15, 10),
        t(16, 10),
        genre=Genre.RNB_SOUL,
        about=(
            "The 'Sweetheart of New Orleans,' Wanda Rouzan has been a beloved\n"
            "entertainer for nearly sixty years. She inherited her band A Taste\n"
            "of New Orleans from the great David Lastie and continues its\n"
            "legacy with a fusion of jazz, blues, funk, soul, and second line\n"
            "that gets everyone on their feet. A regular at French Quarter Fest\n"
            "since 1979, she also holds a Master's degree and teaches Theatre\n"
            "Arts at Audubon Charter School. Featured in HBO's Treme and the\n"
            "film Ray."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://wandarouzan.com/"],
    ),
    Act(
        "Big Frank & Lil Frank & the Dirty Old Men",
        TROPICAL,
        SUN,
        t(16, 30),
        t(17, 45),
        genre=Genre.RNB_SOUL,
        about=(
            "This father-and-son duo has been captivating New Orleans audiences\n"
            "since 2010 with soulful sounds reminiscent of Eddie and Gerald\n"
            "Levert. Big Frank and Lil Frank bring a modern-day energy to\n"
            "classic R&B, channeling influences from The O'Jays, Frankie\n"
            "Beverly & Maze, and Johnnie Taylor. Their live shows at local\n"
            "clubs and festivals consistently deliver an edgy, fresh vibe\n"
            "that commands attention."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[],
    ),
    Act(
        "Honey Island Swamp Band",
        TROPICAL,
        SUN,
        t(18, 15),
        t(19, 45),
        genre=Genre.ROCK,
        about=(
            "Formed in San Francisco in 2005 after displacement from New\n"
            "Orleans by Hurricane Katrina, the Honey Island Swamp Band\n"
            "returned home and built a devoted following with their rootsy\n"
            "blend of blues, soul, country, and New Orleans rhythms. Led by\n"
            "multi-instrumentalist Aaron Wilkinson, their five albums have\n"
            "each been named Roots Rock Album of the Year by Offbeat Magazine.\n"
            "Now celebrating their 20th anniversary, they remain one of the\n"
            "city's most reliable good-time acts."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.honeyislandswampband.com/"],
    ),
    # ── Jack Daniel's Stage ───────────────────────────────────────────
    Act(
        "Roderick 'Rev' Paulin and The Congregation",
        JACKDANIELS,
        SUN,
        t(11, 10),
        t(12, 30),
        genre=Genre.JAZZ_CONTEMPORARY,
        about=(
            "Son of legendary brass band leader Ernest 'Doc' Paulin, Roderick\n"
            "'Rev' Paulin has spent nearly 50 years blending jazz, gospel, and\n"
            "funk into a soul-stirring live experience. A music educator at\n"
            "Southern University and PhD candidate at LSU, he's performed with\n"
            "everyone from John Legend and Allen Toussaint to The Grateful Dead\n"
            "and Trombone Shorty. Rev and the Congregation deliver the spirit\n"
            "of New Orleans with every note."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[],
    ),
    Act(
        "Jason Neville Funky Soul Allstar Band",
        JACKDANIELS,
        SUN,
        t(12, 50),
        t(13, 50),
        genre=Genre.FUNK,
        about=(
            "Jason Neville, youngest son of five-time Grammy winner Aaron\n"
            "Neville and brother of Ivan Neville, formed the FunkySoul Band\n"
            "in 2016. Billed as New Orleans' only LiveMix band, they blend\n"
            "genres on the fly, pairing Jason's powerhouse vocals with the\n"
            "percussion of 'First Lady of Funk' Lirette Dabney Neville, who\n"
            "is also the daughter of jazz legend Sullivan Dabney. From NBA\n"
            "halftime shows to Jazz Fest, the Allstars keep the Neville\n"
            "family legacy burning bright."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://jnevillefunkysoulband.com/"],
    ),
    Act(
        "Gumbeaux Juice",
        JACKDANIELS,
        SUN,
        t(14, 10),
        t(15, 10),
        genre=Genre.MIXED_ECLECTIC,
        about=(
            "Gumbeaux Juice is a rotating hip-hop showcase spotlighting New\n"
            "Orleans rappers and MCs, now a regular feature of the French\n"
            "Quarter Festival. Each year the showcase presents a fresh lineup\n"
            "of local talent, providing a platform for the city's thriving\n"
            "hip-hop scene to share the stage alongside brass bands and jazz\n"
            "legends. Expect high energy, crowd interaction, and a taste of\n"
            "the next generation of New Orleans rap."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[],
    ),
    Act(
        "The Rumble featuring Chief Joseph Boudreaux Jr",
        JACKDANIELS,
        SUN,
        t(15, 30),
        t(16, 30),
        genre=Genre.INDIAN_MARDI_GRAS,
        about=(
            "Fronted by Big Chief Joseph Boudreaux Jr. of the Young Eagles,\n"
            "The Rumble carries forward the vibrant legacy of Mardi Gras\n"
            "Indian funk pioneered by his father Monk Boudreaux and the Wild\n"
            "Magnolias. Formed in 2021, they have already earned two Grammy\n"
            "nominations, including one for their debut 'Live at the Maple\n"
            "Leaf.' Their songs blend Indian chants, brass band traditions,\n"
            "jazz, and hip-hop into a modern sound rooted in the oldest\n"
            "musical traditions of New Orleans."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://therumbleband.com/"],
    ),
    Act(
        "Irma Thomas, Soul Queen of New Orleans",
        JACKDANIELS,
        SUN,
        t(17, 0),
        t(18, 10),
        genre=Genre.RNB_SOUL,
        about=(
            "Officially designated the Soul Queen of New Orleans in 1989,\n"
            "Irma Thomas has been a towering figure in American music for over\n"
            "six decades. A contemporary of Aretha Franklin and Etta James,\n"
            "she finally won her first Grammy in 2007 for After the Rain. Her\n"
            "1964 hit 'Time Is on My Side' predates the Rolling Stones' cover,\n"
            "and in 2024 she joined Mick Jagger on stage at Jazz Fest for a\n"
            "duet of that very song. A living legend who defines New Orleans\n"
            "soul."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[],
    ),
    Act(
        "Cupid & the Dance Party Express Band",
        JACKDANIELS,
        SUN,
        t(18, 40),
        t(20, 0),
        genre=Genre.RNB_SOUL,
        about=(
            "Lafayette, Louisiana native Bryson 'Cupid' Bernard created the\n"
            "global dance phenomenon 'Cupid Shuffle' in 2007, which broke the\n"
            "Guinness World Record for largest line dance with over 17,000\n"
            "people. Since then he has appeared on Dr. Oz, Steve Harvey, and\n"
            "Tom Joyner, and performed everywhere from Germany to Dubai. With\n"
            "his reconstituted Dance Party Express Band, Cupid delivers\n"
            "guaranteed non-stop dancing to close out the festival."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://newcupidonline.com/"],
    ),
    # ── Willow Dispensary Stage ────────────────────────────────────────
    Act(
        "Les Femmes Farouches",
        WILLOW,
        SUN,
        t(11, 10),
        t(12, 20),
        genre=Genre.CAJUN,
        about=(
            "A feisty all-female quartet rooted in traditional Southwestern\n"
            "Louisiana Cajun and Creole music, Les Femmes Farouches feature\n"
            "Michelle Racca-Landry, Natalie Naquin, Katy Murphy, and Sophie\n"
            "Lee. They've become a dance-floor favorite at clubs, festivals,\n"
            "and fais do-dos across New Orleans, regularly packing Three Muses\n"
            "on Frenchmen Street with their infectious two-steps and waltzes."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.instagram.com/lesfemmesfarouches/"],
    ),
    Act(
        "Cameron Dupuy & the Cajun Troubadours",
        WILLOW,
        SUN,
        t(12, 40),
        t(13, 50),
        genre=Genre.CAJUN,
        about=(
            "Eight-time Cajun accordion contest winner Cameron Dupuy started\n"
            "playing accordion at age eleven, inspired by his father Michael\n"
            "Dupuy. A breakout standing-ovation performance at the Liberty\n"
            "Theatre earned the Cajun Troubadours an invitation to Festival\n"
            "Acadiens et Creoles and launched their rise. Their self-titled\n"
            "debut album earned a Grammy nomination for Best Regional Roots\n"
            "Music Album in 2020."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[
            "https://www.cajuntroubadours.com/",
            "https://cajuntroubadours.bandcamp.com/",
        ],
    ),
    Act(
        "Yvette Landry & the Jukes",
        WILLOW,
        SUN,
        t(14, 10),
        t(15, 10),
        genre=Genre.CAJUN,
        about=(
            "Louisiana Music Hall of Famer Yvette Landry didn't pick up a\n"
            "bass guitar until age 40, but she has since earned a Grammy\n"
            "nomination, four albums, and international touring credits. With\n"
            "the Jukes she plays old-school swamp pop inflected with Cajun,\n"
            "Creole, blues, and honky-tonk grooves. A teacher, author, and\n"
            "storyteller from Breaux Bridge, Landry proves it's never too\n"
            "late to follow your musical calling."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://yvettelandry.com/"],
    ),
    Act(
        "Buckwheat Zydeco Jr. & The Legendary Ils Sont Partis Band",
        WILLOW,
        SUN,
        t(15, 30),
        t(16, 40),
        genre=Genre.ZYDECO,
        about=(
            "Following the death of his father, zydeco legend Stanley 'Buckwheat'\n"
            "Dural Sr., in 2016, Buckwheat Zydeco Jr. assumed the mantle of the\n"
            "Ils Sont Partis Band. He grew up next door to Clifton Chenier,\n"
            "joined his father's band at 17, and has since logged over 2,500\n"
            "performances worldwide. In 2024 the band won the Grammy for Best\n"
            "Regional Roots Music Album and was inducted into the Louisiana\n"
            "Music Hall of Fame."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.productionslb.com/"],
    ),
    Act(
        "Chubby Carrier and the Bayou Swamp Band",
        WILLOW,
        SUN,
        t(17, 0),
        t(18, 10),
        genre=Genre.ZYDECO,
        about=(
            "Third-generation zydeco royalty Chubby Carrier started on drums\n"
            "with his father Roy's band at age 12, picked up accordion at 15,\n"
            "and formed his own Bayou Swamp Band in 1989. His album Zydeco\n"
            "Junkie won the Grammy for Best Zydeco or Cajun Music, and he's\n"
            "recorded ten albums over a career that's taken him across the\n"
            "U.S., Canada, North Africa, and Europe. A tireless ambassador\n"
            "for Louisiana's zydeco tradition."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://chubbycarrierzydeco.com/"],
    ),
    Act(
        "Rockin' Dopsie Jr. & the Zydeco Twisters",
        WILLOW,
        SUN,
        t(18, 40),
        t(20, 0),
        genre=Genre.ZYDECO,
        about=(
            "Called the James Brown of Zydeco for his explosive stage energy,\n"
            "Rockin' Dopsie Jr. continues the tradition forged by his father\n"
            "and the legendary Twisters. An accordionist, vocalist, and\n"
            "washboard player, he's performed with Paul Simon, Bob Dylan,\n"
            "and Beyonce, and appeared in the 2024 film Roadhouse. His 2024\n"
            "album 'More Fun With Rockin' Dopsie Jr.' showcases 12 tracks\n"
            "of soul-stirring, body-moving zydeco."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.rockindopsiejr.com/"],
    ),
    # ── Loyola Esplanade in the Shade Stage ───────────────────────────
    Act(
        "Casme",
        LOYOLA,
        SUN,
        t(11, 0),
        t(12, 0),
        genre=Genre.RNB_SOUL,
        about=(
            "New Orleans native Casme is a multi-talented singer, songwriter,\n"
            "dancer, and humanitarian whose powerhouse vocals landed her on\n"
            "Team John Legend on Season 19 of NBC's The Voice. She has opened\n"
            "for Eric Benet, Ginuwine, and Eve, and appeared on Jimmy Kimmel,\n"
            "Jay Leno, and The View. Her latest collection 'Gumbo' spans soul,\n"
            "funk, blues, jazz, hip-hop, and pop. She also runs Casme Cares,\n"
            "a community outreach program feeding hundreds monthly."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.iamcasme.com/"],
    ),
    Act(
        "Across Phoenix, James Wyzten, Kissing Disease",
        LOYOLA,
        SUN,
        t(12, 20),
        t(13, 35),
        genre=Genre.ROCK,
        about=(
            "A triple bill of New Orleans indie bands bringing youthful energy\n"
            "to the Loyola stage. Across Phoenix blends indie rock textures\n"
            "with atmospheric songwriting, while the Kissing Disease, a\n"
            "four-piece formed by Loyola University music students, delivers\n"
            "driving indie rock named after the mononucleosis virus. James\n"
            "Wyzten rounds out the showcase with his own brand of alternative\n"
            "music. Together they represent the city's vibrant emerging scene."
        ),
        about_source=AboutSource.GENERATED,
        websites=[
            "https://acrossphoenix.bandcamp.com/",
            "https://www.thekissingdisease.com/",
        ],
    ),
    Act(
        "Kristin Diable",
        LOYOLA,
        SUN,
        t(13, 55),
        t(14, 50),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "Baton Rouge-born, New Orleans-based singer-songwriter Kristin\n"
            "Diable has been compared to Lucinda Williams for her jazzy,\n"
            "soulful vocal style. She started playing underground clubs as a\n"
            "teenager, moved to New York at 18, then followed her muse back\n"
            "to Louisiana. Her album 'Create Your Own Mythology,' produced\n"
            "by Dave Cobb in Nashville, was applauded by NPR and American\n"
            "Songwriter as one of the year's best. She is also a faculty\n"
            "member at Loyola's College of Music."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://kristindiable.com/"],
    ),
    Act(
        "Helen Gillet: ReBelle Musique",
        LOYOLA,
        SUN,
        t(15, 10),
        t(16, 10),
        genre=Genre.JAZZ_CONTEMPORARY,
        about=(
            "Belgian-born cellist, singer, and composer Helen Gillet moved to\n"
            "New Orleans in 2002 and has since forged a fearlessly eclectic\n"
            "sound using live looping, improvisation, and electronic effects.\n"
            "ReBelle Musique is her tribute to Belgian poet Julos Beaucarne\n"
            "and French chanteuse Brigitte Fontaine, performed with a New\n"
            "Orleans band featuring Alex McMurray on guitar and Rex Gregory\n"
            "on saxophone. She holds a master's in classical cello from Loyola\n"
            "and has spent decades proving cellists belong in jazz bands."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.helengillet.com/"],
    ),
    Act(
        "Creole String Beans",
        LOYOLA,
        SUN,
        t(16, 30),
        t(17, 30),
        genre=Genre.RNB_SOUL,
        about=(
            "A supergroup sextet celebrating the jukebox days of New Orleans\n"
            "rock and roll, the Creole String Beans have been performing since\n"
            "2004. They mix buried treasures from Fats Domino, Frankie Ford,\n"
            "and Dr. John with the swamp pop and R&B that South Louisiana\n"
            "still dances to at weddings and crawfish boils. Their youthful\n"
            "exuberance and faithful renditions have made them a growing\n"
            "favorite at Jazz Fest, French Quarter Festival, and Bayou\n"
            "Boogaloo."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://creolestringbeans.com/"],
    ),
    Act(
        "Astral Project",
        LOYOLA,
        SUN,
        t(17, 50),
        t(19, 0),
        genre=Genre.JAZZ_CONTEMPORARY,
        about=(
            "Founded in 1978 by saxophonist Tony Dagradi, Astral Project has\n"
            "helped shape the New Orleans modern jazz scene for nearly five\n"
            "decades. The quartet features Dagradi, 7-string guitarist Steve\n"
            "Masakowski, bassist James Singleton, and drummer Johnny\n"
            "Vidacovich. Named for Dagradi's interest in Eastern philosophy\n"
            "and the quest for a higher plane of experience, they blend jazz,\n"
            "funk, rock, and world music at their long-running residency at\n"
            "Snug Harbor."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.astralproject.com/"],
    ),
    # ── Louisiana Fish Fry Stage ──────────────────────────────────────
    Act(
        "Smokin' on Some Brass",
        FISHFRY,
        SUN,
        t(11, 10),
        t(12, 20),
        genre=Genre.BRASS_BAND,
        about=(
            "Founded by saxophonist Quay Frazier, Smokin' on Some Brass is\n"
            "a brass, funk, and soul collective redefining contemporary brass\n"
            "band culture in New Orleans. Frazier, a graduate of UNO's jazz\n"
            "studies program and touring member of Corey Henry and the Treme\n"
            "Funktet, brings a fresh perspective to the second line tradition.\n"
            "The collective has quickly earned a reputation for high-energy\n"
            "sets on Frenchmen Street and beyond."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://smokinonsomebrass.com/"],
    ),
    Act(
        "New Birth Brass Band",
        FISHFRY,
        SUN,
        t(12, 40),
        t(14, 0),
        genre=Genre.BRASS_BAND,
        about=(
            "Formed by trumpeter James Andrews to renew the brass band\n"
            "tradition, the New Birth Brass Band was among the first to\n"
            "follow in the footsteps of the pioneering Dirty Dozen and\n"
            "Rebirth. Their first album D-Boy, produced by Allen Toussaint,\n"
            "established their signature fusion of traditional brass with\n"
            "hip-hop, funk, jazz, and Mardi Gras Indian standards. They won\n"
            "the 2001 Big Easy Award for Best Brass Band and continue to\n"
            "energize second line parades across the city."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[],
    ),
    Act(
        "DJ Vintage",
        FISHFRY,
        SUN,
        t(14, 5),
        t(14, 35),
        genre=Genre.ELECTRONIC_DJ,
        about=(
            "DJ Vintage brings curated vinyl-heavy sets of classic funk,\n"
            "soul, rare groove, and New Orleans bounce to the Fish Fry Stage.\n"
            "Part of the city's vibrant DJ culture that stretches from WWOZ\n"
            "radio to Frenchmen Street dance parties, DJ Vintage keeps the\n"
            "crowd moving between the brass band sets with deep cuts and\n"
            "dance-floor favorites."
        ),
        about_source=AboutSource.GENERATED,
        websites=[],
    ),
    Act(
        "Kings of Brass",
        FISHFRY,
        SUN,
        t(14, 40),
        t(16, 0),
        genre=Genre.BRASS_BAND,
        about=(
            "Kings of Brass are a group of New Orleans natives who infuse\n"
            "jazz, funk, hip-hop, R&B, and rock into a new sound rooted in\n"
            "second line culture. Drawing on the city's deep brass band\n"
            "heritage while pushing it forward with contemporary influences,\n"
            "they deliver high-energy sets that honor tradition and innovation\n"
            "in equal measure."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.facebook.com/kobnola/"],
    ),
    Act(
        "DJ ODD Spinz",
        FISHFRY,
        SUN,
        t(16, 5),
        t(16, 35),
        genre=Genre.ELECTRONIC_DJ,
        about=(
            "DJ ODD Spinz, also known as Odd the Artist, is a dynamic female\n"
            "vocalist and DJ who spins and sings across New Orleans at clubs,\n"
            "conferences, and festivals. She weaves her musical tapestry\n"
            "through the heart of the city's diverse traditions, blending\n"
            "bounce, hip-hop, and R&B into crowd-moving sets. Her 2024 release\n"
            "'Let Go, Let Odd' showcases her vocal and production chops."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.wwoz.org/acts/dj-odd-spinz"],
    ),
    Act(
        "Hot 8 Brass Band",
        FISHFRY,
        SUN,
        t(16, 40),
        t(17, 45),
        genre=Genre.BRASS_BAND,
        about=(
            "Formed in 1995 when two earlier bands merged, the Grammy-nominated\n"
            "Hot 8 Brass Band blends hip-hop, jazz, and funk with traditional\n"
            "New Orleans brass. They were propelled to wider fame by Spike\n"
            "Lee's post-Katrina documentary 'When the Levees Broke,' and their\n"
            "lineup of up to ten members delivers a wall of sound that's bigger\n"
            "and bolder than most brass bands. Regulars at Sunday afternoon\n"
            "second line parades and jazz funerals across the city."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["http://www.hot8brassband.com/"],
    ),
    Act(
        "ANTWIGADEE!",
        FISHFRY,
        SUN,
        t(17, 50),
        t(18, 35),
        genre=Genre.ELECTRONIC_DJ,
        about=(
            "ANTWIGADEE, the 'Grooove Master' DJ Antoine Barriere, brings a\n"
            "signature high-energy performance style rooted in New Orleans\n"
            "bounce and global influences. His dynamic sets blend genres and\n"
            "cultures, drawing on the city's deep musical traditions while\n"
            "keeping the crowd dancing with infectious beats and an outsized\n"
            "personality."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[],
    ),
    Act(
        "New Breed",
        FISHFRY,
        SUN,
        t(18, 40),
        t(20, 0),
        genre=Genre.BRASS_BAND,
        about=(
            "Led by Jenard Andrews, son of James 'Twelve' Andrews and nephew\n"
            "of Trombone Shorty, the New Breed Brass Band represents the\n"
            "future of the second line tradition. They made their street debut\n"
            "at the Nine Times Second Line in 2013 and have since released a\n"
            "Grammy-nominated debut 'Made In New Orleans' under Shorty's\n"
            "mentorship. Their adventurous sound fuses Louisiana roots with\n"
            "rock, funk, soul, hip-hop, and Caribbean rhythms. A second Grammy\n"
            "nomination followed for 'Second Line Sunday.'"
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.newbreedbrassband.com/"],
    ),
    # ── Entergy Songwriter Stage ──────────────────────────────────────
    Act(
        "Andy J Forest Treeaux",
        ENTERGY,
        SUN,
        t(11, 0),
        t(11, 55),
        genre=Genre.BLUES,
        about=(
            "Playing harmonica and singing professionally since 1977, Andy J\n"
            "Forest returned to his native New Orleans in 1990 and has been a\n"
            "fixture of the local blues scene ever since. With 23 albums of\n"
            "mostly original songs, he's shared stages with B.B. King, Bobby\n"
            "Blue Bland, and Champion Jack Dupree. Beyond music, he's a\n"
            "published novelist and outsider artist whose paintings depict\n"
            "blues and jazz legends."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://andyjforestmusic.com/"],
    ),
    Act(
        "Luke Allen",
        ENTERGY,
        SUN,
        t(12, 15),
        t(13, 10),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "Luke Spurr Allen is a New Orleans songwriter and frontman of the\n"
            "Happy Talk Band, blending elements of rock, country, folk, and\n"
            "Americana into a dark, wry style. His musical influences include\n"
            "Townes Van Zandt, Leonard Cohen, and Nick Cave. A regular on the\n"
            "local club circuit and festival scene, Allen brings literary\n"
            "songcraft and understated charisma to the Entergy Songwriter\n"
            "Stage."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://lukespurrallen.com/"],
    ),
    Act(
        "Justin Garner",
        ENTERGY,
        SUN,
        t(13, 30),
        t(14, 25),
        genre=Genre.RNB_SOUL,
        about=(
            "From Plaquemine, Louisiana, Justin Garner honed his vocal\n"
            "abilities in the Baptist church before building a global audience\n"
            "through original songs and YouTube covers. His rich blend of R&B\n"
            "and soul has topped iTunes charts in multiple countries. He has\n"
            "sung the National Anthem for the Saints, Giants, Spurs, and\n"
            "Chiefs, and in 2026 will perform at both French Quarter Fest and\n"
            "a Jazz Fest tribute to Frankie Beverly & Maze."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.justingarner.com/"],
    ),
    Act(
        "Bobbi Rae",
        ENTERGY,
        SUN,
        t(14, 45),
        t(15, 45),
        genre=Genre.RNB_SOUL,
        about=(
            "Rooted in Slidell, Louisiana, Bobbi Rae discovered singing in\n"
            "the church and has built a career as a powerful contemporary R&B\n"
            "and neo-soul artist. Her soul-stirring alto-soprano range earned\n"
            "her a deal with Warner Brothers for her debut single. She has\n"
            "toured Brazil, performing at major festivals, and recently\n"
            "released the collaboration 'Nobody Knows' with MacInfinity.\n"
            "Her live performances fuse inspirational energy with razor-sharp\n"
            "vocal precision."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://therealbobbirae.com/"],
    ),
    Act(
        "Cristina Kaminis",
        ENTERGY,
        SUN,
        t(16, 5),
        t(17, 0),
        genre=Genre.WORLD,
        about=(
            "Mexican-American singer Cristina Kaminis grew up between Mexico\n"
            "City and Miami before spending a dozen years in New York, then\n"
            "moving to New Orleans in 2021. Singing in seven languages and\n"
            "backed by a band of Brazilian musicians, she is equally at home\n"
            "with bolero, samba, ranchera, and Great American Songbook\n"
            "standards. Her debut album 'Temperance' reflects the many\n"
            "cultural layers of her music and life."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.cristinakaminismusic.com/"],
    ),
    # ── Pan-American Life Insurance Group Stage ───────────────────────
    Act(
        "Bamboula 2000",
        PANAMLIFE,
        SUN,
        t(11, 10),
        t(12, 10),
        genre=Genre.WORLD,
        about=(
            "Founded by percussionist Luther Gray in 1994, Bamboula 2000 is\n"
            "an African drumming and dance collective rooted in historic Congo\n"
            "Square. Integrating modern soul with African, Caribbean, and jazz\n"
            "influences, they've won the Big Easy Award for Best World Music\n"
            "Group three times and been nominated eight more. The group also\n"
            "reaches thousands of children annually through their 'Imagination\n"
            "Tour' drum and dance workshops."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["http://www.bamboula2000.com/"],
    ),
    Act(
        "Anaïs St. John",
        PANAMLIFE,
        SUN,
        t(12, 30),
        t(13, 30),
        genre=Genre.RNB_SOUL,
        about=(
            "New Orleans native Anaïs St. John was trained as an opera singer\n"
            "at Xavier University, singing mezzo-soprano with the New Orleans\n"
            "Opera before branching out as a solo artist blending jazz, blues,\n"
            "and R&B. Inspired by Eartha Kitt, Irma Thomas, and Germaine\n"
            "Bazzle, she has developed sultry tribute shows honoring Donna\n"
            "Summer and Tina Turner. She also holds a Master's degree and\n"
            "teaches music at Trinity Episcopal School."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[],
    ),
    Act(
        "Papo y Son Mandao",
        PANAMLIFE,
        SUN,
        t(13, 50),
        t(14, 50),
        genre=Genre.LATIN,
        about=(
            "Led by guitarist and vocalist Alexis 'Papo' Munoz Guevara, born\n"
            "in Yaguajay, Cuba, in 1964, Papo y Son Mandao delivers Latin\n"
            "jazz, salsa, cha-cha-cha, and son cubano to New Orleans stages.\n"
            "The quartet features Israel Romo on percussion, Julian Alpizar\n"
            "on bass, and Omar Ramirez on trumpet. A regular at WWOZ and the\n"
            "French Quarter Festival, they bring authentic Cuban rhythms to\n"
            "the Crescent City."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.facebook.com/papoysonmandao/"],
    ),
    Act(
        "Los Güiros",
        PANAMLIFE,
        SUN,
        t(15, 10),
        t(16, 10),
        genre=Genre.LATIN,
        about=(
            "Los Guiros blend psychedelic cumbia with New Orleans flair,\n"
            "fusing Colombian folkloric dance rhythms and Peruvian chicha\n"
            "with modern electronic elements. Vocalist Corina Hernandez sings\n"
            "over Todd Burdick's thundering sousaphone (he moonlights from\n"
            "Tuba Skinny), giving the traditional cumbia sound a uniquely NOLA\n"
            "twist. Their monthly cumbia dance party at the Saturn Bar is\n"
            "one of the hottest tickets in town."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://losguiros.com/", "https://losguiros.bandcamp.com/"],
    ),
    Act(
        "Stanton Moore featuring Joe Ashlar and Danny Abel",
        PANAMLIFE,
        SUN,
        t(16, 30),
        t(17, 50),
        genre=Genre.FUNK,
        about=(
            "Galactic's legendary drummer Stanton Moore teams with organist\n"
            "Joe Ashlar and guitarist Danny Abel for an intimate, groove-heavy\n"
            "trio format. Born out of their popular Happy Organ Hour series at\n"
            "the Maple Leaf Bar, this collaboration strips the funk down to its\n"
            "essentials: deep-pocket drumming, Hammond B-3 swells, and Abel's\n"
            "searing guitar work. Abel has also toured with Big Freedia and\n"
            "The Revivalists."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[
            "https://www.mapleleafbar.com/",
            "https://www.dannyabel.com/",
        ],
    ),
    Act(
        "Leyla McCalla",
        PANAMLIFE,
        SUN,
        t(18, 10),
        t(19, 30),
        genre=Genre.WORLD,
        about=(
            "Haitian-American multi-instrumentalist Leyla McCalla plays cello,\n"
            "tenor banjo, and guitar with stunning mastery, singing in English,\n"
            "French, and Haitian Creole. A former cellist with the Carolina\n"
            "Chocolate Drops and founding member of Our Native Daughters with\n"
            "Rhiannon Giddens, she came to New Orleans to busk on French\n"
            "Quarter streets with Bach's Cello Suites. Her critically acclaimed\n"
            "album 'Vari-Colored Songs' adapts Langston Hughes poems alongside\n"
            "Haitian folk songs and originals."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://leylamccalla.com/"],
    ),
    # ── Jazz Playhouse at the Royal Sonesta ───────────────────────────
    Act(
        "Jenna McSwain Jazz Band",
        JAZZPLAYHOUSE,
        SUN,
        t(11, 0),
        t(13, 30),
        genre=Genre.JAZZ_CONTEMPORARY,
        about=(
            "Pianist, vocalist, and composer Jenna McSwain leads her sisters\n"
            "through spirituals in the South Carolina low country before\n"
            "becoming an active player in the Charleston jazz scene. She holds\n"
            "a Master's in Jazz Studies and is now a full-time professor at\n"
            "Loyola University New Orleans. Her bold musical choices span\n"
            "classic and contemporary jazz, Brazilian music, and progressive\n"
            "rock with her band Bionica. She has opened for Patti Austin and\n"
            "Ramsey Lewis."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://jennamcswain.com/"],
    ),
    Act(
        "Jeanne Marie Harris",
        JAZZPLAYHOUSE,
        SUN,
        t(14, 0),
        t(16, 30),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Jeanne-Marie Harris brings a warm, expressive voice to the\n"
            "standards of the Great American Songbook. A graduate of Belmont\n"
            "University in Nashville, she gained rare perspective on both the\n"
            "creative and business sides of music before settling in New\n"
            "Orleans. She performs with acclaimed ensembles including the Shim\n"
            "Sham Band and the Nola Dukes, breathing new life into beloved\n"
            "standards in both trio and full-band settings."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://jeanne-mariemusic.com/"],
    ),
    Act(
        "Gerald French & The Original Tuxedo Jazz Band",
        JAZZPLAYHOUSE,
        SUN,
        t(17, 0),
        t(19, 30),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "The Original Tuxedo Jazz Band is the oldest established jazz band\n"
            "in the world, organized in 1910 by Oscar 'Papa' Celestin and the\n"
            "first jazz band to play the White House in 1953. Gerald 'The\n"
            "Giant' French is a third-generation leader of the band, following\n"
            "his grandfather Albert 'Papa' French. An accomplished drummer\n"
            "and vocalist, Gerald has shared the stage with Dr. John, Harry\n"
            "Connick Jr., and Preservation Hall Jazz Band."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.geraldfrench.com/"],
    ),
    # ── French Market Traditional Jazz Stage ──────────────────────────
    Act(
        "Smoking Time Jazz Club",
        FRENCHMARKET,
        SUN,
        t(11, 30),
        t(13, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "One of the leaders in the renaissance of New Orleans traditional\n"
            "jazz, the Smoking Time Jazz Club revives and refreshes the music\n"
            "of the 1920s and '30s. Vocalist Sarah Peterson pays tribute to\n"
            "the inflections of early jazz originators while making the sound\n"
            "her own. The band has maintained a tight lineup through long-\n"
            "running weekly gigs at the Spotted Cat and The Maison, and has\n"
            "recorded over 90 tracks. Nominated by Offbeat for Best\n"
            "Traditional Jazz Band."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["http://www.smokingtimejazzclub.com/"],
    ),
    Act(
        "Charlie Halloran and the Tropicales",
        FRENCHMARKET,
        SUN,
        t(13, 30),
        t(15, 0),
        genre=Genre.WORLD,
        about=(
            "Named a rising star by Downbeat and one of the city's top\n"
            "trombonists by Offbeat, Charlie Halloran leads the Tropicales\n"
            "in a musical cruise through the Caribbean from a New Orleans\n"
            "home port. Their 1950s hotel-party vibe features torrid horns\n"
            "and tropical rhythms from Trinidad to Guadeloupe, nodding to\n"
            "New Orleans' history as the northernmost Caribbean port. Their\n"
            "2024 album 'Jump Up' features guest vocalists Cyrille Aimee\n"
            "and Quiana Lynell."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.charliehalloran.com/"],
    ),
    Act(
        "The New Orleans Swinging Gypsies",
        FRENCHMARKET,
        SUN,
        t(15, 30),
        t(17, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Bandleader John Saavedra's Swinging Gypsies blend gypsy jazz,\n"
            "traditional jazz, and swing with a punk rock edge. Their\n"
            "foundation is the Django Reinhardt guitar style filtered through\n"
            "New Orleans influences and a modern sensibility. A unique feature\n"
            "is tap dancer Giselle Anguizola, whose percussive flamenco-\n"
            "flavored footwork adds a visual and rhythmic dimension that sets\n"
            "the band apart on the festival circuit."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://swinginggypsies.com/"],
    ),
    Act(
        "Sullivan Dabney's Muzik Jazz Band",
        FRENCHMARKET,
        SUN,
        t(17, 30),
        t(19, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Professional drummer and vocalist Sullivan Dabney started the\n"
            "Muzik Jazz Band in 1972 and has been a staple at French Quarter\n"
            "Fest and Jazz Fest ever since, plus international festivals in\n"
            "the UK, Germany, and Switzerland. His style synthesizes jazz\n"
            "dialects, R&B, and New Orleans phrasings into a crowd-pleasing\n"
            "blend. He toured with Ernie K-Doe for five years and has played\n"
            "with Irma Thomas, Eddie Bo, and Jean Knight."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[],
    ),
    # ── French Market Dutch Alley Stage ───────────────────────────────
    Act(
        "Hot Club of New Orleans",
        DUTCHALLEY,
        SUN,
        t(11, 15),
        t(12, 30),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Featuring guitarist Russell Welch, who excels in the gypsy jazz\n"
            "stylings of Django Reinhardt, the Hot Club of New Orleans channels\n"
            "the spirit of the Quintette du Hot Club de France through a\n"
            "distinctly New Orleans lens. Welch's impeccable fretwork and the\n"
            "band's acoustic string instrumentation evoke the hot jazz and\n"
            "swing of the 1930s while keeping things fresh for contemporary\n"
            "audiences on Frenchmen Street and beyond."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.russellwelch.com/"],
    ),
    Act(
        "Mayumi Shara & New Orleans Jazz Letters",
        DUTCHALLEY,
        SUN,
        t(12, 45),
        t(14, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Japanese-American drummer Mayumi Shara is a pioneer of female\n"
            "jazz drumming in Japan who moved to New Orleans in 1998, studying\n"
            "funk and R&B drumming under Jeffrey 'Jelly Bean' Alexander. She\n"
            "leads the N.O. Jazz Letters, as well as the all-Japanese women's\n"
            "blues band Pink Magnolias and Taiko drum ensemble MaDeTo. Her\n"
            "cross-cultural approach to traditional jazz brings a unique\n"
            "perspective to the New Orleans scene."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://about.me/mayumishara"],
    ),
    Act(
        "Jade Perdue",
        DUTCHALLEY,
        SUN,
        t(14, 15),
        t(15, 30),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "New Orleans native Jade Perdue is a versatile vocalist and\n"
            "instrumentalist who grew up singing in church and playing in\n"
            "the Edna Karr High School marching band. After earning her music\n"
            "degree from Xavier University, she was hired by the National Park\n"
            "Service as an interpretive ranger for jazz, performing traditional\n"
            "jazz, blues, and funk with the Arrowhead Jazz Band. She regularly\n"
            "shares the bandstand with Herlin Riley and Nicholas Payton at the\n"
            "New Orleans Jazz Museum."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.jadesantrell.com/"],
    ),
    Act(
        "Tom Saunders and the Hotcats",
        DUTCHALLEY,
        SUN,
        t(15, 45),
        t(17, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Bass, tuba, and bass saxophonist Tom Saunders leads the Hotcats,\n"
            "a five-piece ensemble performing authentic 1920s traditional jazz.\n"
            "Saunders also helms the Tomcats, a larger hot big band format\n"
            "that captures the era when hot jazz was giving birth to swing.\n"
            "Both bands deliver the spontaneity and fire of the great jazz\n"
            "age while maintaining a polished ensemble sound."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[],
    ),
    # ── House of Blues Voodoo Garden Stage ─────────────────────────────
    Act(
        "Sophia Parigi",
        HOUSEOFBLUES,
        SUN,
        t(12, 30),
        t(14, 30),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Sophia Parigi is a versatile vocalist and self-accompanied\n"
            "pianist performing jazz standards, Songbook classics, New Orleans\n"
            "music, show tunes, and pop. A product of NOCCA, she entertains\n"
            "as a solo act or with a jazz combo, bringing an intimate\n"
            "cocktail-lounge vibe to the Voodoo Garden."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.sophiaparigi.com/"],
    ),
    Act(
        "Sean Riley",
        HOUSEOFBLUES,
        SUN,
        t(15, 0),
        t(17, 0),
        genre=Genre.BLUES,
        about=(
            "New Orleans blues and roots singer-songwriter Sean Riley\n"
            "references Delta blues and Americana with contemporary themes.\n"
            "A familiar face from the Bywater to the French Quarter and\n"
            "Uptown, he plays solo and with his fluid backing band The Water,\n"
            "touring extensively in Europe and Australia as well. His debut\n"
            "full-length 'Stone Cold Hands' established him as a distinctive\n"
            "voice in the modern Southern blues tradition."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.seanrileyandthewater.com/"],
    ),
    # ── New Orleans Jazz National Historical Park Stage ────────────────
    Act(
        "Craig Klein's New Orleans Allstars",
        JAZZPARK,
        SUN,
        t(11, 0),
        t(12, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Grammy-winning trombonist Craig Klein has played professionally\n"
            "in New Orleans for over 40 years and appeared on more than 200\n"
            "recordings with legends like Dr. John and the Neville Brothers.\n"
            "A founding member of the Storyville Stompers, the Nightcrawlers,\n"
            "and Bonerama, he assembles his Allstars from the cream of the\n"
            "city's jazz talent for a set rooted in the traditional New\n"
            "Orleans sound."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.craigkleinmusic.com/"],
    ),
    Act(
        "Matt Lemmler presents 'New Orleans in Stride'",
        JAZZPARK,
        SUN,
        t(12, 15),
        t(13, 15),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Jazz piano professor at Loyola University, Matt Lemmler presents\n"
            "New Orleans stride piano, a slower, loping cousin to the New York\n"
            "style with an underlying triple-meter feel most associated with\n"
            "James Booker. After touring with Phantom of the Opera and earning\n"
            "a graduate degree from Manhattan School of Music, he returned\n"
            "home to play with Bob French's Original Tuxedo Jazz Band and\n"
            "Pete Fountain. It took Hurricane Katrina for him to share his\n"
            "soulful singing voice with the world."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.mattlemmler.com/"],
    ),
    Act(
        "Crescent City Sisters",
        JAZZPARK,
        SUN,
        t(13, 30),
        t(14, 30),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "The Crescent City Sisters carry on the tradition of all-female\n"
            "jazz ensembles in New Orleans, performing traditional jazz, swing,\n"
            "and early blues. Drawing from the city's deep well of musical\n"
            "heritage, they bring a spirited, soulful energy to the Jazz\n"
            "National Historical Park stage, honoring the women who helped\n"
            "shape New Orleans music from its earliest days."
        ),
        about_source=AboutSource.GENERATED,
        websites=[],
    ),
    Act(
        "Louis Ford",
        JAZZPARK,
        SUN,
        t(14, 45),
        t(15, 45),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Fifth-generation New Orleans musician Louis Ford carries on the\n"
            "legacy of his father Clarence Ford, who performed with Fats\n"
            "Domino. The family's musical lineage traces back to 1856 and\n"
            "includes cousins like Charlie Gabriel of Preservation Hall Jazz\n"
            "Band. Trained under Ellis Marsalis at NOCCA and a graduate of\n"
            "Loyola's music program, Ford is one of the foremost practitioners\n"
            "of traditional jazz clarinet and performs regularly at\n"
            "Preservation Hall."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://fordmusicproductions.com/"],
    ),
    Act(
        "Arrowhead Jazz Band feat. NPS Rangers et al.",
        JAZZPARK,
        SUN,
        t(16, 0),
        t(17, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "The Arrowhead Jazz Band is the resident ensemble of the New\n"
            "Orleans Jazz National Historical Park, bringing together NPS\n"
            "rangers and local musicians to perform traditional New Orleans\n"
            "jazz, blues, and gospel. Rangers Jade Perdue, Matt Hampsey,\n"
            "Kerry Lewis Sr., and Hunter Miles Davis anchor the band, with\n"
            "special guests rotating through for each performance. A free,\n"
            "living expression of the park's mission to celebrate jazz."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://home.nps.gov/jazz/learn/arrowhead-jazz-band.htm"],
    ),
    # ── Ernie's Schoolhouse Stage ─────────────────────────────────────
    Act(
        "Greater New Orleans Youth Orchestras",
        SCHOOLHOUSE,
        SUN,
        t(11, 0),
        t(12, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "The Greater New Orleans Youth Orchestras provide classical and\n"
            "jazz training to young musicians across the metro area, offering\n"
            "a showcase for the next generation of New Orleans talent."
        ),
        about_source=AboutSource.GENERATED,
        websites=[],
    ),
    Act(
        "Chalmette High School Marching Band",
        SCHOOLHOUSE,
        SUN,
        t(12, 20),
        t(13, 20),
        genre=Genre.BRASS_BAND,
        about=(
            "Chalmette High School's marching band represents St. Bernard\n"
            "Parish's strong tradition of music education, bringing youthful\n"
            "energy and school spirit to the Schoolhouse Stage."
        ),
        about_source=AboutSource.GENERATED,
        websites=[],
    ),
    Act(
        "St. Mary's Academy Gospel Choir",
        SCHOOLHOUSE,
        SUN,
        t(13, 50),
        t(14, 50),
        genre=Genre.GOSPEL,
        about=(
            "St. Mary's Academy Gospel Choir carries on the deep gospel\n"
            "tradition of New Orleans, with student voices raised in spirited\n"
            "praise on the Schoolhouse Stage."
        ),
        about_source=AboutSource.GENERATED,
        websites=[],
    ),
    Act(
        "Don Jamison Heritage School of Music",
        SCHOOLHOUSE,
        SUN,
        t(15, 10),
        t(16, 10),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "The Don Jamison Heritage School of Music cultivates young\n"
            "musicians in the New Orleans jazz tradition, ensuring the city's\n"
            "musical heritage is passed to the next generation."
        ),
        about_source=AboutSource.GENERATED,
        websites=[],
    ),
    Act(
        "Walter L. Cohen High School Marching Band",
        SCHOOLHOUSE,
        SUN,
        t(16, 30),
        t(17, 30),
        genre=Genre.BRASS_BAND,
        about=(
            "Walter L. Cohen High School's marching band brings the spirit\n"
            "and pride of New Orleans public school music programs to the\n"
            "festival's Schoolhouse Stage."
        ),
        about_source=AboutSource.GENERATED,
        websites=[],
    ),
    # ── Hancock Whitney Stage ─────────────────────────────────────────
    Act(
        "Kid Merv & All That Jazz",
        HANCOCK,
        SUN,
        t(11, 30),
        t(12, 45),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Born Mervin Campbell, Kid Merv was dubbed by the late Milton\n"
            "Batiste in honor of Kid Rena after his split from the Soul Rebels\n"
            "in 1997. His debut CD won two Offbeat Awards, and his trumpet\n"
            "has graced the Olympia Brass Band, Treme Brass Band, and the\n"
            "Louis Armstrong Society Band. A sought-after combo leader, Kid\n"
            "Merv is a regular at Satchmo SummerFest, Jazz Fest, and French\n"
            "Quarter Festival."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[],
    ),
    Act(
        "Miss Sophie Lee",
        HANCOCK,
        SUN,
        t(13, 0),
        t(14, 15),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "The self-styled 'Seoul Queen,' Miss Sophie Lee moved to New\n"
            "Orleans in 2001 and built her musical life on Frenchmen Street,\n"
            "where she first sang traditional jazz 15 years ago. Born in\n"
            "Chicago to a Korean mother and a Black father with Mississippi\n"
            "roots, she defies the trad jazz category with inflections of\n"
            "reggae, funk, and soul. She is also proprietor of the popular\n"
            "Three Muses restaurant and music club."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://misssophielee.com/"],
    ),
    Act(
        "Mark Brooks",
        HANCOCK,
        SUN,
        t(14, 30),
        t(15, 45),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Versatile bassist and singer Mark Brooks holds down the groove\n"
            "at storied venues from Preservation Hall to Fritzel's Jazz Pub.\n"
            "A protege of the late Alvin Batiste at Southern University, he\n"
            "has performed with Dr. John, the Neville Brothers, Lou Rawls,\n"
            "and Fats Domino's band. His film and TV credits include Clint\n"
            "Eastwood's Bridges of Madison County, the Ray Charles biopic,\n"
            "HBO's Roots, and Interview with the Vampire."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://markabrooks.net/"],
    ),
    Act(
        "New Orleans High Society",
        HANCOCK,
        SUN,
        t(16, 0),
        t(17, 15),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "New Orleans High Society is a traditional jazz band based in the\n"
            "Crescent City that creates fresh arrangements of classic songs\n"
            "while incorporating gospel, Afro-Cuban, and modern R&B\n"
            "influences. Their contemporary sensibility keeps the traditional\n"
            "jazz sound vital and danceable for audiences who appreciate both\n"
            "deep history and creative reinterpretation."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://nohighsociety.com/"],
    ),
    # ── Omni Royal Orleans Stage ──────────────────────────────────────
    Act(
        "Jason Mingledorff",
        OMNI,
        SUN,
        t(11, 15),
        t(12, 30),
        genre=Genre.JAZZ_CONTEMPORARY,
        about=(
            "One of the most versatile and in-demand saxophonists in New\n"
            "Orleans since 1995, Jason Mingledorff has played with Galactic,\n"
            "Papa Grows Funk, Dr. John, and Harry Connick Jr. He won a Grammy\n"
            "with the Nightcrawlers Brass Band for 'Atmosphere' in 2020 and\n"
            "teaches saxophone and conducts the jazz workshop at Loyola\n"
            "University. His 2023 debut solo album 'Start It!' showcases\n"
            "nine original compositions of melodic, bluesy tenor saxophone."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.jasonmingledorff.com/"],
    ),
    Act(
        "Father Ron and Friends",
        OMNI,
        SUN,
        t(12, 45),
        t(14, 0),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "Retired Episcopal priest and WWOZ folk DJ Father Ron Clingenpeel\n"
            "leads a group of talented musicians who give voice to traditional\n"
            "American folk music. With Robert Eustis on guitar, David Schwartz\n"
            "on keyboards, Barbara Smith-Davis on vocals, and Max Valentino\n"
            "on bass, they balance polished musicianship with approachable\n"
            "charm. Their album 'Forever The Seasons' won a Bronze Medal at\n"
            "the Global Music Awards."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.fatherronandfriends.com/"],
    ),
    Act(
        "Sweetie Pies of New Orleans",
        OMNI,
        SUN,
        t(14, 15),
        t(15, 30),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "The Sweetie Pies of New Orleans serve up a joyful mix of pre-war\n"
            "blues, traditional jazz, and jug band music. Vocalist Becky Lynn\n"
            "Blanca delivers vintage-flavored vocals alongside guitarist\n"
            "Russell Welch, a master of the Django Reinhardt style who also\n"
            "fronts the Hot Club of New Orleans. The band is a staple at the\n"
            "Spotted Cat and DBA, blending Mississippi blues roots with the\n"
            "rhythms of New Orleans jazz."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[],
    ),
    Act(
        "Ecirb Müller's Twisted Dixie",
        OMNI,
        SUN,
        t(15, 45),
        t(17, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Ecirb Muller is the alter ego of veteran trumpeter and educator\n"
            "Dr. Brice Miller, whose Twisted Dixie takes traditional jazz\n"
            "and updates it with elements of pop, hip-hop, go-go, swing,\n"
            "dub-step, and free jazz in a style he calls NuTrad. The band\n"
            "is the only one in New Orleans where all members are teachers,\n"
            "including two university professors. Their monthly shows at the\n"
            "Spotted Cat regularly draw lines down the street."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://twisteddixienola.com/"],
    ),
    # ── KREWE Eyewear Stage ───────────────────────────────────────────
    Act(
        "Capivaras Jazz Quartet",
        KREWE,
        SUN,
        t(11, 0),
        t(12, 15),
        genre=Genre.WORLD,
        about=(
            "The Capivaras Jazz Quartet blends Brazilian bossa nova, samba,\n"
            "and jazz traditions with the musical culture of New Orleans.\n"
            "Part of the city's growing Brazilian music community, the\n"
            "quartet brings warm harmonies and sophisticated rhythms that\n"
            "reflect both South American and Gulf Coast sensibilities."
        ),
        about_source=AboutSource.GENERATED,
        websites=[],
    ),
    Act(
        "The New Orleans Jazz Vipers",
        KREWE,
        SUN,
        t(12, 30),
        t(13, 45),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Founded in 1999 by alto saxophonist Joe Braun, the Jazz Vipers\n"
            "were the first band to play the now-renowned Spotted Cat Music\n"
            "Club. Their early swing sound features hard-driving acoustic\n"
            "rhythm and spirited horns with a punk sensibility, notably\n"
            "without a drum kit. Braun's original 'I Hope You're Coming\n"
            "Back to New Orleans' was featured in HBO's Treme and included\n"
            "on the Grammy-nominated soundtrack."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.neworleansjazzvipers.com/"],
    ),
    Act(
        "Seva Venet's Traditional Line-Up",
        KREWE,
        SUN,
        t(14, 0),
        t(15, 15),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Banjoist and guitarist Seva Venet channels the spirits of Danny\n"
            "Barker and Django Reinhardt through his deep immersion in the\n"
            "New Orleans traditional jazz community. After moving from Los\n"
            "Angeles at the turn of the century, he studied under Tuba Fats,\n"
            "joined the Treme Brass Band, and played alongside Lionel Ferbos.\n"
            "Today he performs with Dr. Michael White, Greg Stafford's Jazz\n"
            "Hounds, and his own ensembles, and is a key figure in the Danny\n"
            "Barker Guitar and Banjo Festival."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://sevavenet.com/"],
    ),
    Act(
        "Harry Mayronne & Chloe Marie",
        KREWE,
        SUN,
        t(15, 30),
        t(16, 45),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Pianist Harry Mayronne is the go-to partner for many New Orleans\n"
            "singers and theatre productions, as well as a world-renowned\n"
            "marionettist. Vocalist Chloe Marie moved from Baton Rouge during\n"
            "the pandemic and sings with the Victory Belles and under her own\n"
            "name in indie folk and soul. Together, their intimate piano-and-\n"
            "voice format breathes new life into standards at cocktail bars\n"
            "like the Bombay Club."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://harrymayronne.com/"],
    ),
    # ── Cafe Beignet Stage ────────────────────────────────────────────
    Act(
        "Steamboat Willy",
        CAFEBEIGNET,
        SUN,
        t(11, 30),
        t(14, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "A publicly performing musician since 1972, Steamboat Willie\n"
            "earned his nickname during a gig in Biloxi and has been a French\n"
            "Quarter fixture for decades. Leading on cornet and vocals, he\n"
            "fronts a rotating ensemble of clarinet, trombone, tuba, and\n"
            "drums, delivering traditional Dixieland jazz from his home base\n"
            "at Cafe Beignet on Bourbon Street and the Musical Legends Park.\n"
            "He started playing cornet in church bands at age eight."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[],
    ),
    Act(
        "Steve Rohbock Trio",
        CAFEBEIGNET,
        SUN,
        t(14, 30),
        t(17, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Pianist and vocalist Steve Rohbock is a familiar presence in the\n"
            "New Orleans traditional jazz world, performing regularly at\n"
            "Musical Legends Park and other French Quarter venues. His trio\n"
            "format highlights classic jazz piano stylings and standards,\n"
            "providing the perfect acoustic backdrop for a lazy Sunday\n"
            "afternoon at Cafe Beignet."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[],
    ),
]
