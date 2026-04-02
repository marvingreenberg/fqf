"""Friday April 17, 2026 — FQF schedule data.

DEPRECATED: This file is no longer the authoritative source of schedule data.
The canonical data lives in src/fqf/data/fq2026_acts.yaml.
This file is kept for reference only and is not imported by the package.
"""

from fqf.models import (
    ABITA,
    DUTCHALLEY,
    ENTERGY,
    FISHFRY,
    FRENCHMARKET,
    FRI,
    HOUSEOFBLUES,
    JACKDANIELS,
    JAZZPLAYHOUSE,
    LOYOLA,
    NEWORLEANS,
    PANAMLIFE,
    TROPICAL,
    WILLOW,
    AboutSource,
    Act,
    Genre,
    t,
)

FRIDAY_ACTS: list[Act] = [
    # ── Abita Beer Stage ──────────────────────────────────────────────
    Act(
        "Bo Dollis Jr. and the Wild Magnolias",
        ABITA,
        FRI,
        t(11, 30),
        t(12, 30),
        genre=Genre.INDIAN_MARDI_GRAS,
        about=(
            "Big Chief Bo Dollis Jr. carries on one of the deepest traditions in\n"
            "New Orleans as leader of the Wild Magnolias, a Mardi Gras Indian\n"
            "tribe whose masking legacy stretches back to the 1950s. He took the\n"
            "reins from his father, NEA Heritage Fellow Bo Dollis Sr., and blends\n"
            "Mardi Gras Indian chanting with heavy funk grooves. Their album\n"
            "Chip Off the Old Block fuses Indian traditions with Memphis soul.\n"
            "Expect feathered suits, call-and-response chants, and a groove\n"
            "that will have the whole crowd moving."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.wildmagnoliasfunk.com/"],
    ),
    Act(
        "Irvin Mayfield",
        ABITA,
        FRI,
        t(12, 50),
        t(13, 50),
        genre=Genre.JAZZ_CONTEMPORARY,
        about=(
            "Grammy and Billboard Award-winning trumpeter Irvin Mayfield is\n"
            "one of New Orleans' most decorated jazz ambassadors. A native of\n"
            "the city, he picked up his first trumpet in fourth grade and went\n"
            "on to found Los Hombres Calientes and the New Orleans Jazz\n"
            "Orchestra. His collaborators range from Frank Ocean and Lenny\n"
            "Kravitz to Wynton Marsalis and Dr. John. Whether leading a\n"
            "tight combo or a full orchestra, Mayfield channels the deep\n"
            "lineage of New Orleans trumpet masters."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.basinstreetrecords.com/artists/irvin-mayfield/"],
    ),
    Act(
        "The Dixie Cups",
        ABITA,
        FRI,
        t(14, 10),
        t(15, 10),
        genre=Genre.RNB_SOUL,
        about=(
            "Sisters Barbara Ann and Rosa Lee Hawkins, along with cousin Joan\n"
            "Marie Johnson, shot to number one in 1964 with the irresistible\n"
            "Chapel of Love, knocking The Beatles off the top of the charts.\n"
            "Raised in New Orleans' Calliope housing project, the trio helped\n"
            "define the girl-group sound of the 1960s. They also recorded the\n"
            "Mardi Gras classic Iko Iko. Decades later they still bring that\n"
            "joyful energy to festival stages."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://dixiecups.bandcamp.com/"],
    ),
    Act(
        "Bonerama",
        ABITA,
        FRI,
        t(15, 30),
        t(16, 30),
        genre=Genre.FUNK,
        about=(
            "Bonerama puts trombones front and center in a way nobody else\n"
            "does. Founded in 1998 by Mark Mullins and Craig Klein, both\n"
            "former members of Harry Connick Jr.'s big band, the group fuses\n"
            "rock, funk, brass, and blues into a wall of low-end power.\n"
            "The current lineup features three trombones, guitar, sousaphone,\n"
            "and drums. They have collaborated with R.E.M. and Tom Morello,\n"
            "and their Plays Zeppelin album was a Jazz Fest bestseller."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.boneramabrass.com/"],
    ),
    Act(
        "Jon Cleary & the Absolute Monster Gentlemen",
        ABITA,
        FRI,
        t(16, 50),
        t(18, 10),
        genre=Genre.FUNK,
        about=(
            "British-born pianist Jon Cleary moved to New Orleans and never\n"
            "looked back, absorbing the city's funk, R&B, and piano traditions\n"
            "until they became second nature. His Grammy-winning album Go Go\n"
            "Juice cemented his reputation as a master of the New Orleans\n"
            "keyboard groove. Backed by the Absolute Monster Gentlemen, a\n"
            "crack rhythm section of New Orleans natives, Cleary delivers\n"
            "shows that swing from Professor Longhair-style piano workouts to\n"
            "deep soul ballads. A Tipitina's and Jazz Fest mainstay."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.joncleary.com/"],
    ),
    Act(
        "PJ Morton",
        ABITA,
        FRI,
        t(18, 40),
        t(20, 0),
        genre=Genre.RNB_SOUL,
        about=(
            "New Orleans native PJ Morton wears many hats: six-time Grammy\n"
            "winner, keyboardist for Maroon 5, solo R&B artist, and founder\n"
            "of Morton Records, which he envisioned as a New Orleans Motown.\n"
            "His solo work, from the acclaimed Gumbo to Cape Town to Cairo,\n"
            "blends classic soul songwriting with modern production while\n"
            "staying rooted in the musical traditions of his hometown.\n"
            "Closing out the Abita stage on Friday, Morton brings a headliner\n"
            "set packed with silky grooves and gospel-tinged power."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.instagram.com/pjmorton/"],
    ),
    # ── NewOrleans.com Stage ──────────────────────────────────────────
    Act(
        "John Boutté",
        NEWORLEANS,
        FRI,
        t(11, 15),
        t(12, 25),
        genre=Genre.JAZZ_CONTEMPORARY,
        about=(
            "John Boutté's voice is the sound of New Orleans itself. Born\n"
            "into a 7th Ward Creole-Catholic family, he grew up steeped in\n"
            "jazz funerals, Mardi Gras parades, and the R&B of Stevie Wonder\n"
            "and Marvin Gaye. His Treme Song became the theme of HBO's Treme,\n"
            "making him an ambassador for the city's post-Katrina resilience.\n"
            "His repertoire crosses jazz, R&B, gospel, Latin, and blues with\n"
            "effortless warmth. Sister Lillian Boutté is also a renowned\n"
            "singer, making music a family affair."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.wwoz.org/acts/john-boutte"],
    ),
    Act(
        "Don Vappie and the Creole Jazz Serenaders",
        NEWORLEANS,
        FRI,
        t(12, 45),
        t(14, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Don Vappie is a Creole master of the tenor banjo and a pillar of\n"
            "traditional New Orleans jazz. A Banjo Hall of Fame inductee and\n"
            "recipient of the Steve Martin Banjo Prize, he is also Wynton\n"
            "Marsalis' go-to banjoist. The Creole Jazz Serenaders, his\n"
            "arranging outlet turned full jazz orchestra, have been a fixture\n"
            "at Jazz Fest for over twenty years. Vappie's album The Bluebook\n"
            "of Storyville was named 2020 Album of the Year by The Times of\n"
            "London. Deep, swinging, and steeped in Creole heritage."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.donvappie.com/"],
    ),
    Act(
        "Lawrence Cotton Legendary Experience",
        NEWORLEANS,
        FRI,
        t(14, 20),
        t(15, 30),
        genre=Genre.RNB_SOUL,
        about=(
            "At 99, pianist Lawrence Cotton is New Orleans' oldest working\n"
            "musician and a living link to the golden age of rhythm and blues.\n"
            "Born in 1927 in Uptown, he backed Guitar Slim from 1954 to 1958\n"
            "and played with Dave Bartholomew, Joe Turner, and T-Bone Walker.\n"
            "Named a Master Practitioner by the Preservation Hall Foundation,\n"
            "Cotton leads his own band with the steady swing and irrepressible\n"
            "joy of someone who has spent a lifetime making people dance."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://salon726.com/home/meet-the-collective-lawrence-cotton"],
    ),
    Act(
        "Kyle Roussel's Church of New Orleans",
        NEWORLEANS,
        FRI,
        t(15, 50),
        t(17, 0),
        genre=Genre.RNB_SOUL,
        about=(
            "Pianist Kyle Roussel, from Boutte, Louisiana, holds down the\n"
            "keys for the Preservation Hall Jazz Band and channels a lifetime\n"
            "of gospel, classical, and jazz training into his own projects.\n"
            "His Grammy-nominated album Church of New Orleans features Irma\n"
            "Thomas, Ivan Neville, and John Boutté, weaving the New Orleans\n"
            "piano tradition with street beats and sacred-music roots.\n"
            "Roussel studied under legends Alvin Batiste and Ellis Marsalis\n"
            "Jr. at NOCCA and UNO. Expect a soulful, spirit-lifting set."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.kyleroussel.com/"],
    ),
    Act(
        "Robin Barnes & The Fiya Birds",
        NEWORLEANS,
        FRI,
        t(17, 20),
        t(18, 45),
        genre=Genre.FUNK,
        about=(
            "Robin Barnes, the Songbird of New Orleans, brings the power of\n"
            "a soul revival with the spirit and funk of her hometown. A native\n"
            "of the Lower Ninth Ward, Barnes debuted at number five on the\n"
            "Billboard Traditional Jazz Albums chart and has performed at\n"
            "venues worldwide, including London's Royal Opera House. With\n"
            "The Fiya Birds, she delivers a high-energy blend that draws\n"
            "comparisons to Chaka Khan meets Ella Fitzgerald. Named Best\n"
            "Local Artist/Band by Gambit in 2024."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://robinbarnesmusic.com/"],
    ),
    # ── Tropical Isle Hand Grenade Stage ──────────────────────────────
    Act(
        "Maji Melodies - Semaj & The Blues Experiment",
        TROPICAL,
        FRI,
        t(11, 10),
        t(12, 10),
        genre=Genre.BLUES,
        about=(
            "Semaj and The Blues Experiment serve up a mashup of rock, soul,\n"
            "hip-hop, and funk energy fused with classic covers and originals.\n"
            "Based in New Orleans, the group performs regularly at venues like\n"
            "St. Roch Market and NOMA Friday Nights, building a following\n"
            "through relentless gigging and genre-blending sets. Under the\n"
            "Maji Melodies banner, the act channels blues tradition through\n"
            "a modern, eclectic lens."
        ),
        about_source=AboutSource.RESEARCHED,
    ),
    Act(
        "Joe Lastie's Jazz to Brass feat. Dr. Pathorn",
        TROPICAL,
        FRI,
        t(12, 30),
        t(13, 30),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Drummer Joe Lastie Jr. comes from one of New Orleans' most\n"
            "beloved musical dynasties. A Preservation Hall Jazz Band member\n"
            "since 1989, he studied at the Dryades Street YMCA alongside\n"
            "young Wynton and Branford Marsalis. His Jazz to Brass project\n"
            "bridges traditional jazz and brass band styles, honoring a\n"
            "family legacy that helped bring drumming into the New Orleans\n"
            "spiritual church. Here he is joined by Dr. Pathorn for a set\n"
            "steeped in the city's oldest musical traditions."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.joelastie.com/"],
    ),
    Act(
        "Ashton Hines and the Big Easy Brawlers",
        TROPICAL,
        FRI,
        t(13, 50),
        t(14, 50),
        genre=Genre.BRASS_BAND,
        about=(
            "Trumpeter Ashton Hines, a McDonogh 35 Marching Band alumnus,\n"
            "helped build the foundation for the Frenchmen Street live music\n"
            "scene. The Big Easy Brawlers blend New Orleans brass with funk,\n"
            "soul, hip-hop, and footwork, delivering shows packed with dance\n"
            "routines, epic solos, crowd surfing, and motivational speeches.\n"
            "Their path from street performance to main stages paved the way\n"
            "for a generation of New Orleans musicians."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://smokinonsomebrass.com/"],
    ),
    Act(
        "Sally Baby's Silver Dollars",
        TROPICAL,
        FRI,
        t(15, 10),
        t(16, 10),
        genre=Genre.RNB_SOUL,
        about=(
            "Fronted by Salvatore Geloso, Sally Baby's Silver Dollars play\n"
            "a fresh take on retro New Orleans R&B dance-hall music and Creole\n"
            "jazz. They rose quickly from busking and tiny dives to an NPR\n"
            "Tiny Desk Concert in early 2026, after finishing as runner-up in\n"
            "the 2024 competition. Their self-titled debut EP, recorded at\n"
            "Big Tone Studios, captures the band's inherently funky, timeless\n"
            "sound. One of the most exciting new acts in the city."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://sallybaby.bandcamp.com/"],
    ),
    Act(
        "Deezle",
        TROPICAL,
        FRI,
        t(16, 30),
        t(17, 45),
        genre=Genre.RNB_SOUL,
        about=(
            "New Orleans native Darius Harrison, known as Deezle, is a\n"
            "three-time Grammy Award-winning songwriter, producer, and\n"
            "engineer who co-produced Lil Wayne's smash hit Lollipop. Deeply\n"
            "shaped by the city's bounce and hip-hop culture, he has worked\n"
            "with Drake, Nicki Minaj, J-Lo, and Chris Brown. In recent years\n"
            "Deezle has stepped from the control room to center stage as a\n"
            "performer in his own right, blending R&B vocals with his\n"
            "production expertise."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[
            "https://www.sofndopemagazine.com/post/deezle-from-the-control-room-to-center-stage-r-b-s-next-leading-man-emerges"
        ],
    ),
    Act(
        "Lisa Amos",
        TROPICAL,
        FRI,
        t(18, 15),
        t(19, 45),
        genre=Genre.RNB_SOUL,
        about=(
            "Born and raised in New Orleans, Lisa Amos inherited her musical\n"
            "drive from her mother, a force on the local music scene. Her\n"
            "seductive vocals and compassionate songwriting weave R&B and\n"
            "soul into a tapestry of emotion. Regulars at the Zulu Club know\n"
            "her Saturday night sets with The Royal Essence Show Band. With\n"
            "singles like You Used to Love Me and Love Me Now Baby, Amos\n"
            "brings polished, danceable soul to the Tropical Isle stage."
        ),
        about_source=AboutSource.RESEARCHED,
    ),
    # ── Jack Daniel's Stage ───────────────────────────────────────────
    Act(
        "Khris Royal and Dark Matter",
        JACKDANIELS,
        FRI,
        t(11, 10),
        t(12, 30),
        genre=Genre.MIXED_ECLECTIC,
        about=(
            "Saxophonist Khris Royal is a genre-defying force. A New Orleans\n"
            "native who earned a full scholarship to Berklee at 16, he leads\n"
            "Dark Matter through jazz, funk, rock, hip-hop, and soul with\n"
            "the intensity of a rock show. The band doubles as Big Freedia's\n"
            "backing group, so they know a thing or two about getting crowds\n"
            "moving. Royal is a Grammy-nominated multi-instrumentalist who\n"
            "plays sax, bass, keys, and DJ sets, and has shared stages with\n"
            "Ellis Marsalis, Branford Marsalis, and Bobby Brown."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://khrisroyal.band/home"],
    ),
    Act(
        "Cole Williams",
        JACKDANIELS,
        FRI,
        t(12, 50),
        t(13, 50),
        genre=Genre.RNB_SOUL,
        about=(
            "Jamaican-American entertainer Cole Williams blends R&B, rap,\n"
            "gospel, and world beats into music that celebrates humanity and\n"
            "hope. She hosts The New Orleans Music Show on WWOZ 90.7 FM and\n"
            "founded The Greater New Orleans Citizens Relief Team, focusing\n"
            "on issues facing the houseless. Her original Give Power to the\n"
            "People and a stirring rendition of Sam Cooke's A Change is Gonna\n"
            "Come showcase a voice used as an agent for social change. She has\n"
            "appeared on NCIS: New Orleans and Big Freedia Means Business."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://colewilliamsmusic.com/"],
    ),
    Act(
        "The Iguanas",
        JACKDANIELS,
        FRI,
        t(14, 10),
        t(15, 10),
        genre=Genre.WORLD,
        about=(
            "Formed in 1989 around vocalist and guitarist Rod Hodges, The\n"
            "Iguanas have spent three decades fusing Tex-Mex, Conjunto, Latin\n"
            "styles, blues, zydeco, Cajun, and roots rock into an exotic,\n"
            "mesmerizing groove. Based in New Orleans since the mid-1990s,\n"
            "the band's members have collectively played with Charlie Rich,\n"
            "Alex Chilton, Emmylou Harris, and Allen Toussaint. Their dance\n"
            "floors fill fast and stay packed."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.iguanas.com/"],
    ),
    Act(
        "People Museum",
        JACKDANIELS,
        FRI,
        t(15, 30),
        t(16, 40),
        genre=Genre.MIXED_ECLECTIC,
        about=(
            "People Museum is a pop-art electronic quartet born in the Treme\n"
            "neighborhood, blending Afrobeat, hip-hop, choral, and marching\n"
            "band influences into bright indie-pop soundscapes. Trombonist\n"
            "Jeremy Phipps and singer Claire Givens co-founded the group in\n"
            "2016, later joined by Aaron Boudreaux and Charles Lumar II.\n"
            "They have shared stages with Thundercat and Big Freedia, and\n"
            "even performed with the Louisiana Philharmonic Orchestra.\n"
            "Genre-bending music that could only come from New Orleans."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.peoplemuseumband.com/"],
    ),
    Act(
        "LSD Clown System",
        JACKDANIELS,
        FRI,
        t(17, 0),
        t(18, 20),
        genre=Genre.ELECTRONIC_DJ,
        about=(
            "LSD Clownsystem is a clown-themed LCD Soundsystem tribute act\n"
            "that has become a genuine New Orleans phenomenon. A collective\n"
            "of top local musicians, costume artists, and DJs, they deck out\n"
            "in full clown makeup and deliver immersive, top-tier renditions\n"
            "of dance-punk anthems with New Orleans-flavored twists, honks,\n"
            "and bonks. What started as a joke for a 2018 cover-band show\n"
            "has grown into must-see events like Big Top Ball and 20,000\n"
            "Clowns Under the Sea."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.lsdclownsystem.com/"],
    ),
    Act(
        "The Dirty Dozen Brass Band",
        JACKDANIELS,
        FRI,
        t(18, 50),
        t(20, 0),
        genre=Genre.BRASS_BAND,
        about=(
            "Established in 1977 and rooted in Danny Barker's youth music\n"
            "program at Fairview Baptist Church, the Dirty Dozen Brass Band\n"
            "revolutionized brass band music by incorporating funk and bebop\n"
            "into the traditional New Orleans style. Their 2023 Grammy for\n"
            "Best American Roots Performance caps a career spanning five\n"
            "continents, twelve studio albums, and collaborations from Modest\n"
            "Mouse to Norah Jones. They gave brass bands worldwide visibility\n"
            "and remain the gold standard."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["http://dirtydozenbrassband.com/"],
    ),
    # ── Willow Dispensary Stage ────────────────────────────────────────
    Act(
        "T Marie and Bayou Juju",
        WILLOW,
        FRI,
        t(11, 10),
        t(12, 20),
        genre=Genre.CAJUN,
        about=(
            "T Marie and Bayou Juju play traditional and original Louisiana\n"
            "music with fresh interpretations of Cajun, Creole, Zydeco, Swamp\n"
            "Pop, and blues, performed in both Louisiana French and English.\n"
            "The trio of T Marie on fiddle and vocals, Adam Bellard on\n"
            "accordion and guitar, and Brennan Breaux on percussion grew out\n"
            "of front-porch gatherings and levee jams. Their debut album hit\n"
            "the initial Grammy ballot for Best Regional Roots Music and\n"
            "topped Bandcamp's Cajun/Zydeco chart."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://tmarieandbayoujuju.bandcamp.com/"],
    ),
    Act(
        "T'Canaille",
        WILLOW,
        FRI,
        t(12, 40),
        t(13, 50),
        genre=Genre.CAJUN,
        about=(
            "T'Canaille is a New Orleans-based Cajun band that plays\n"
            "everything from traditional Cajun two-steps to something a\n"
            "little more rocking, with a dash of Zydeco thrown in. Featuring\n"
            "Lance Caruso on accordion and vocals, Jason Crosby on fiddle,\n"
            "and Chris Senac on bass, the trio are favorites at the Tropical\n"
            "Isle Bayou Club and French Market Festival. Friendly, energetic,\n"
            "and always ready to get the dance floor moving."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://tcanaille.wordpress.com/"],
    ),
    Act(
        "B. Cam & The Zydeco Young Bucks",
        WILLOW,
        FRI,
        t(14, 10),
        t(15, 10),
        genre=Genre.ZYDECO,
        about=(
            "B. Cam and The Zydeco Young Bucks represent the next generation\n"
            "of zydeco, bringing youthful energy and fresh grooves to a\n"
            "tradition built on accordion, rubboard, and infectious rhythms.\n"
            "Making their French Quarter Fest debut in 2026, the group has\n"
            "been building a following on the Louisiana and Texas zydeco\n"
            "circuit. Catch them early for a high-energy dance party."
        ),
        about_source=AboutSource.GENERATED,
    ),
    Act(
        "Lost Bayou Ramblers",
        WILLOW,
        FRI,
        t(15, 30),
        t(16, 40),
        genre=Genre.CAJUN,
        about=(
            "Brothers Andre and Louis Michot formed the Lost Bayou Ramblers\n"
            "in 1999 to carry on the roots Cajun music of their family band\n"
            "Les Freres Michot, then proceeded to blow the genre wide open.\n"
            "Their sound fuses old-world Louisiana French traditions with\n"
            "rockabilly swagger, punk energy, and psychedelia, all sung in\n"
            "Cajun French. Two-time Grammy winners, they contributed to the\n"
            "Oscar-nominated film Beasts of the Southern Wild and Jack\n"
            "White's American Epic project."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://lostbayouramblers.com/"],
    ),
    Act(
        "Sunpie and the Louisiana Sunspots",
        WILLOW,
        FRI,
        t(17, 0),
        t(18, 10),
        genre=Genre.ZYDECO,
        about=(
            "Bruce Sunpie Barnes pioneered a unique style he calls\n"
            "Afro-Louisiana music, mixing zydeco, blues, gospel, jazz, and\n"
            "African and Caribbean sounds into a musical gumbo. A former\n"
            "NFL player turned park ranger, naturalist, and musician, he\n"
            "plays accordion, harmonica, trombone, and more. Since 2010 he\n"
            "has also led the Northside Skull and Bones Gang, a legendary\n"
            "Mardi Gras group dating to 1819. Six albums and over fifty\n"
            "countries toured with the Louisiana Sunspots."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.sunpiebarnes.live/"],
    ),
    Act(
        "Brass-A-Holics",
        WILLOW,
        FRI,
        t(18, 40),
        t(20, 0),
        genre=Genre.BRASS_BAND,
        about=(
            "Since 2010, trombonist Winston Turner's Brass-A-Holics have\n"
            "taken a heavy dose of Washington D.C. go-go funk and injected it\n"
            "into the New Orleans brass band sound. Turner built his chops at\n"
            "St. Augustine High School's Marching 100 and spent twelve years\n"
            "with the Soul Rebels before striking out on his own. The band\n"
            "adds electric bass, guitar, and a full drum kit to traditional\n"
            "brass, covering everything from Louis Armstrong to Lil Wayne.\n"
            "High-energy dance music guaranteed."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://thebrassaholics.com/"],
    ),
    # ── Loyola Esplanade in the Shade Stage ───────────────────────────
    Act(
        "Kirkland Green",
        LOYOLA,
        FRI,
        t(11, 0),
        t(12, 0),
        genre=Genre.RNB_SOUL,
        about=(
            "Kirkland Green is a New Orleans-based singer-songwriter from\n"
            "central Louisiana who grew up singing in church and found his\n"
            "voice in musical theatre before channeling Gospel, Soul, Jazz,\n"
            "and R&B into his own Neo-Soul world. Often seen fronting KG and\n"
            "the Analog Machine on Frenchmen Street, he made his Jazz Fest\n"
            "and Bayou Boogaloo debuts in 2025. Beyond performing, he directs\n"
            "arts education programs for young children through Mess Arts."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://kirklandgreenmusic.com/"],
    ),
    Act(
        "Tuller, Not Related, Liam Escame, and Surco",
        LOYOLA,
        FRI,
        t(12, 20),
        t(13, 35),
        genre=Genre.MIXED_ECLECTIC,
        about=(
            "This multi-artist showcase brings together four rising acts from\n"
            "the New Orleans scene. Tuller and Surco both appeared at the\n"
            "2024 NOLA Funk Fest, representing the city's indie and Latin-\n"
            "tinged sounds. Liam Escame is a young saxophonist studying at\n"
            "Loyola University who has been making a name on the local jazz\n"
            "circuit. Not Related rounds out the bill. Together they offer\n"
            "a snapshot of the city's emerging musical talent."
        ),
        about_source=AboutSource.GENERATED,
    ),
    Act(
        "The RiverBenders",
        LOYOLA,
        FRI,
        t(13, 55),
        t(14, 50),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "The RiverBenders are a roots-Americana trio featuring Aaron\n"
            "Wilkinson of Honey Island Swamp Band, Jake Eckert of the Dirty\n"
            "Dozen Brass Band and New Orleans Suspects, and Myles Weeks, who\n"
            "has played with James Hunter and Andrew Duhon. Three premier\n"
            "songwriters and performers collaborating in a stripped-down\n"
            "format, the group delivers warm, crafted songs rooted in New\n"
            "Orleans' deep musical soil. Featured at Jazz Fest 2026."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["http://riverbendersnola.com/"],
    ),
    Act(
        "Pellow Talk & Alfred Banks",
        LOYOLA,
        FRI,
        t(15, 10),
        t(16, 10),
        genre=Genre.MIXED_ECLECTIC,
        about=(
            "Pellow Talk is the DJ and producer alter ego of New Orleans\n"
            "rapper Pell, known for his infectious blend of alternative\n"
            "hip-hop, R&B, and electronic textures. Alfred Banks is an\n"
            "award-winning rapper and singer who has become one of the most\n"
            "recognizable voices in New Orleans hip-hop, featured on The\n"
            "Fader, HipHopDx, and Okayplayer. Their joint EP The Survivor's\n"
            "Condition pairs atmospheric production with introspective bars.\n"
            "Together they bridge hip-hop, soul, and indie sensibilities."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[
            "http://pellyeah.com/",
            "https://www.underdogcentral.com/presskit",
        ],
    ),
    Act(
        "New Orleans Legacy Coalition",
        LOYOLA,
        FRI,
        t(16, 30),
        t(17, 30),
        genre=Genre.BRASS_BAND,
        about=(
            "The New Orleans Legacy Coalition draws from the deep well of\n"
            "the city's marching band tradition. Connected to the New Orleans\n"
            "Legacy Association of Bands, a community organization that\n"
            "fosters music education and supports band programs, the group\n"
            "channels the energy of second lines and parade culture into a\n"
            "festival-ready performance. Expect rousing brass, tight\n"
            "percussion, and the unmistakable spirit of New Orleans street\n"
            "music."
        ),
        about_source=AboutSource.GENERATED,
        websites=["https://www.nolalegacybands.org/"],
    ),
    Act(
        "Cha Wa",
        LOYOLA,
        FRI,
        t(17, 50),
        t(19, 0),
        genre=Genre.INDIAN_MARDI_GRAS,
        about=(
            "Cha Wa, whose name means we're comin' for ya in Mardi Gras\n"
            "Indian parlance, is a Grammy-nominated funk collective that\n"
            "fuses the primal chants and percussion of Mardi Gras Indian\n"
            "traditions with brass band grooves, hip-hop beats, and soulful\n"
            "vocals. Formed in 2014 by drummer Joe Gelini, the band features\n"
            "frontman Honey Bannister in stunning traditional Indian regalia.\n"
            "Their albums Spyboy and My People both earned Grammy nods. Wild,\n"
            "colorful, and impossible to stand still for."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["http://www.chawaband.com/"],
    ),
    # ── Louisiana Fish Fry Stage ──────────────────────────────────────
    Act(
        "Magnetic Ear",
        FISHFRY,
        FRI,
        t(11, 10),
        t(12, 20),
        genre=Genre.BRASS_BAND,
        about=(
            "Magnetic Ear is a six-piece original brass band led by German-\n"
            "born saxophonist and instrument repairman Martin Krusche, who\n"
            "has made New Orleans his home. Their mostly original music is\n"
            "inspired by New Orleans second-line and funk, Eastern European\n"
            "brass band traditions, and African rhythms. With tenor and\n"
            "baritone sax, two trombones, sousaphone, and drums, they turn\n"
            "cerebral compositions into irresistible dance-floor material."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.magneticear.com/"],
    ),
    Act(
        "Tidal Wave Brass Band",
        FISHFRY,
        FRI,
        t(12, 40),
        t(14, 0),
        genre=Genre.BRASS_BAND,
        about=(
            "Founded in 2022 by trumpeter John Perkins, a University of New\n"
            "Orleans Jazz Studies graduate who has performed with Rebirth\n"
            "Brass Band, Stooges Brass Band, and Preservation Hall, Tidal\n"
            "Wave Brass Band was created to bring magical experiences through\n"
            "music. The five-piece ensemble covers everything from gospel to\n"
            "rock, jazz to Caribbean, and has quickly built a reputation for\n"
            "joyous second-line energy at festivals and events."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["http://tidalwavebrassband.com/"],
    ),
    Act(
        "DJ ChiNola",
        FISHFRY,
        FRI,
        t(14, 5),
        t(14, 35),
        genre=Genre.ELECTRONIC_DJ,
        about=(
            "DJ ChiNola is a New Orleans-based DJ originally from Chicago\n"
            "who has built a following with creative genre-blending sets.\n"
            "A regular on the French Quarter Fest lineup, ChiNola keeps the\n"
            "energy high between brass band sets on the Fish Fry stage with\n"
            "a deep crate of grooves. The name says it all: Chicago roots,\n"
            "New Orleans soul."
        ),
        about_source=AboutSource.RESEARCHED,
    ),
    Act(
        "Young Pinstripe Brass Band",
        FISHFRY,
        FRI,
        t(14, 40),
        t(16, 0),
        genre=Genre.BRASS_BAND,
        about=(
            "The Young Pinstripe Brass Band carries on the legacy of the\n"
            "storied Pinstripe Brass Band dynasty, incorporating classic and\n"
            "contemporary sounds from New Orleans jazz and funk to soul,\n"
            "rock, and hip-hop. Managed by Herbert Young, the band is a\n"
            "perennial at Jazz Fest and a go-to for second-line parades,\n"
            "jazz funerals, and celebrations. Expect tight horn lines, heavy\n"
            "bass drum, and the kind of groove that makes New Orleans move."
        ),
        about_source=AboutSource.RESEARCHED,
    ),
    Act(
        "Kidd Love",
        FISHFRY,
        FRI,
        t(16, 5),
        t(16, 35),
        genre=Genre.ELECTRONIC_DJ,
        about=(
            "Turntablist, producer, and underground music lover Kidd Love\n"
            "first picked up turntables at age twelve, inspired by legends\n"
            "like Mix Master Mike, Qbert, and Jazzy Jeff. Based in New\n"
            "Orleans, he competes in world-renowned DJ battles like Red Bull\n"
            "Threestyle and DMC, and hosts weekly residencies at Dragon's\n"
            "Den. A sharp selector who bridges hip-hop, funk, and electronic\n"
            "sounds with vinyl-digging authenticity."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://kiddlove.bandcamp.com/"],
    ),
    Act(
        "Treme Brass Band",
        FISHFRY,
        FRI,
        t(16, 40),
        t(17, 45),
        genre=Genre.BRASS_BAND,
        about=(
            "Founded in the early 1990s by drummer Benny Jones Sr., the\n"
            "Treme Brass Band is the gold standard for traditional New\n"
            "Orleans brass band music. Members wear the classic uniform of\n"
            "band caps and white shirts, practice collective improvisation\n"
            "and call-and-response, and anchor the city's second-line parades\n"
            "and jazz funerals. Recipients of a National Heritage Fellowship\n"
            "from the NEA, they are living guardians of a sacred tradition."
        ),
        about_source=AboutSource.RESEARCHED,
    ),
    Act(
        "DJ Polo504",
        FISHFRY,
        FRI,
        t(17, 50),
        t(18, 35),
        genre=Genre.ELECTRONIC_DJ,
        about=(
            "Justin Polo504 Smith has been the connection between music and\n"
            "entertainment since he started spinning at age twelve. A premier\n"
            "nightlife DJ in New Orleans, his extensive library spans Motown,\n"
            "disco, R&B, bounce, hip-hop, reggaeton, and EDM. Known for his\n"
            "infectious voice and turntable skills, Polo504 keeps dance\n"
            "floors packed at celebrity events, clubs, and festivals. When\n"
            "not commanding crowds at home, he travels the world delivering\n"
            "his explosive sound."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.djpolo504.com/"],
    ),
    Act(
        "Sporty's Brass Band",
        FISHFRY,
        FRI,
        t(18, 40),
        t(20, 0),
        genre=Genre.BRASS_BAND,
        about=(
            "Led by trombonist Maurice Sporty Craig, a former member of the\n"
            "Stooges Brass Band, Sporty's Brass Band has earned a reputation\n"
            "for heart-pounding energy and uncontrollable dancing. The nine-\n"
            "piece ensemble fuses classic street parade rhythms with funk,\n"
            "jazz, and soul, performing at everything from weddings to jazz\n"
            "funerals. Regulars at the Hi-Ho Lounge and Brass Hall on\n"
            "Decatur Street, they have played Jazz Fest, French Quarter Fest,\n"
            "and Mardi Gras, and were featured in the New York Post."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://sportysbrassband.com/"],
    ),
    # ── Entergy Songwriter Stage ──────────────────────────────────────
    Act(
        "Don Paul and Rivers Answer Moons",
        ENTERGY,
        FRI,
        t(11, 0),
        t(11, 55),
        genre=Genre.MIXED_ECLECTIC,
        about=(
            "Don Paul is a poet, author, and activist who leads Rivers Answer\n"
            "Moons, a visionary New Orleans ensemble blending spoken-word\n"
            "poetry with jazz, funk, and roots music. The band features\n"
            "saxophone legend Roger Lewis of the Dirty Dozen Brass Band,\n"
            "master drummer Herlin Riley, and sousaphonist Kirk Joseph.\n"
            "Their double album Louisiana Stories weaves vivid poetic\n"
            "narratives with genre-crossing arrangements. On stage, expect\n"
            "an immersive experience shaped by the city's sonic traditions."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://donpaul1.bandcamp.com/"],
    ),
    Act(
        "Lisbon Girls",
        ENTERGY,
        FRI,
        t(12, 15),
        t(13, 10),
        genre=Genre.ROCK,
        about=(
            "Lisbon Girls are a New Orleans indie rock trio of siblings\n"
            "Lucho, Pilar, and Nikolai. Their songs, sung in Spanish, draw\n"
            "on 1980s Japanese city pop while weaving in Latin and folkloric\n"
            "percussion that reflects their heritage. Their album Te Love\n"
            "You dropped in 2024, and the band made its Jazz Fest debut in\n"
            "2025. A fresh, bilingual voice in the city's indie scene."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://lisbongirls1.bandcamp.com/"],
    ),
    Act(
        "Kelly Love Jones",
        ENTERGY,
        FRI,
        t(13, 30),
        t(14, 25),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "New Orleans-born singer-songwriter Kelly Love Jones is a multi-\n"
            "instrumentalist, producer, and director whose music blends R&B,\n"
            "soul, folk, hip-hop, and reggae into something deeply personal.\n"
            "A Big Easy Award winner, Louisiana Music Ambassador, and United\n"
            "Nations Appointed Messenger of Truth, she has opened for Lenny\n"
            "Kravitz and Meshell Ndegeocello. Her recent album Surrender\n"
            "captures the spirit of her live shows, where she wields an\n"
            "acoustic guitar and cajon with intimate, healing energy."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.kellylovejonesmusic.com/"],
    ),
    Act(
        "Johnny Sansone",
        ENTERGY,
        FRI,
        t(14, 45),
        t(15, 40),
        genre=Genre.BLUES,
        about=(
            "Johnny Sansone is a Blues Music Award-winning harmonica player,\n"
            "accordionist, and songwriter who settled in New Orleans in 1990\n"
            "after years as an itinerant bluesman. He studied under harmonica\n"
            "legends James Cotton and Junior Wells, and has toured with John\n"
            "Lee Hooker and Ronnie Earl. His blistering electric harmonica\n"
            "tone and swamp-roots accordion give his twelve albums a\n"
            "distinctly Louisiana flavor. A life-changing Howlin' Wolf show\n"
            "at age twelve set the course for his career."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.johnnysansone.com/"],
    ),
    Act(
        "Max Bien-Kahn",
        ENTERGY,
        FRI,
        t(16, 0),
        t(17, 0),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "San Francisco-born Max Bien-Kahn has called New Orleans home\n"
            "for over fourteen years, busking traditional jazz and classic\n"
            "country on the streets before developing a solo catalog that\n"
            "blends swamp pop, sixties rock, folk, and modern indie. He plays\n"
            "tenor banjo in the beloved trad-jazz outfit Tuba Skinny, and\n"
            "his fourth solo album Flowers came out in late 2024. Witty,\n"
            "melodic, and cathartic, his songwriting feels like partying to\n"
            "someone's diary."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.maxbienkahn.com/"],
    ),
    # ── Pan-American Life Insurance Group Stage ───────────────────────
    Act(
        "Lulu and the Broadsides",
        PANAMLIFE,
        FRI,
        t(11, 0),
        t(12, 10),
        genre=Genre.RNB_SOUL,
        about=(
            "Lulu and the Broadsides is fronted by singer-songwriter Dayna\n"
            "Kurtz and backed by a supergroup of New Orleans musicians:\n"
            "James Singleton on bass, Carlo Nuccio on drums, Glenn Hartman\n"
            "on keys, and Robert Mache on guitar. The band slings made-for-\n"
            "dancing vintage R&B with the emphasis on rhythm, mining rock and\n"
            "roll, blues, and soul. Formed to feed New Orleans' underground\n"
            "dance scene, they bring deep-pitched, honeyed vocals that\n"
            "smolder over tight grooves."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://luluandthebroadsides.com/"],
    ),
    Act(
        "Arsène Delay & Charlie Wooton",
        PANAMLIFE,
        FRI,
        t(12, 30),
        t(13, 30),
        genre=Genre.MIXED_ECLECTIC,
        about=(
            "Arsene DeLay is a vocal powerhouse from the musical Boutte\n"
            "family, related to jazz singers Lillian and John Boutte. Her\n"
            "repertoire mixes originals with the New Orleans canon, heavily\n"
            "tinged by gospel, jazz, and rock. Charlie Wooton is a Lafayette-\n"
            "born bassist and songwriter who has played with Bonerama, Cyril\n"
            "Neville, and Sonny Landreth. Together they blend roots, funk,\n"
            "and soul into a set that spans the breadth of Louisiana music.\n"
            "Both are seasoned festival performers with global touring\n"
            "credits."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[
            "https://www.arsenedelaymusic.com/",
            "http://www.charliewooton.com/",
        ],
    ),
    Act(
        "Dusky Waters",
        PANAMLIFE,
        FRI,
        t(13, 50),
        t(14, 50),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "Dusky Waters is the stage name of Jenn Jeffers, a contemporary\n"
            "Americana songwriter whose clarion-call vocals and intricate\n"
            "banjo and guitar work ebb and flow like the Mississippi. She\n"
            "fuses gospel, folk, and soul traditions with modern pop melodies,\n"
            "honoring the South while forging a new path. As co-founder and\n"
            "Executive Director of BlackAmericana Fest, she champions Black\n"
            "artists in Americana, folk, and country music. A rising voice\n"
            "in New Orleans' rootsy singer-songwriter circle."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.duskywaters.com/"],
    ),
    Act(
        "Amigos do Samba",
        PANAMLIFE,
        FRI,
        t(15, 10),
        t(16, 10),
        genre=Genre.WORLD,
        about=(
            "Amigos do Samba is a traditional Brazilian samba band based in\n"
            "New Orleans whose mission is to bring the roda de samba, the\n"
            "communal street-and-backyard samba tradition of Rio de Janeiro,\n"
            "to the Crescent City. They play traditional samba, pagode, and\n"
            "songs by the legendary 1970s Rio band Fundo de Quintal, using\n"
            "a variety of Brazilian percussion and string instruments played\n"
            "around a table. Interactive, joyful, and irresistibly danceable."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.facebook.com/amigosdosambanola/"],
    ),
    Act(
        "Camile Baudoin and Friends",
        PANAMLIFE,
        FRI,
        t(16, 30),
        t(17, 20),
        genre=Genre.ROCK,
        about=(
            "Native New Orleanian Camile Baudoin spent over forty-five years\n"
            "as lead guitarist for The Radiators, defining the fishhead music\n"
            "sound with his funk-driven rhythms, powerful slide work, and\n"
            "incendiary solos. Inducted into the Louisiana Music Hall of\n"
            "Fame, he now gigs prolifically with Raw Oyster Cult, Fishhead\n"
            "Stew, and The Gatorators. His latest release This Old House\n"
            "celebrates the New Orleans dance party tradition. A living\n"
            "legend of Crescent City rock."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["http://camilebaudoin.com/"],
    ),
    Act(
        "Bill Summers & Jazalsa",
        PANAMLIFE,
        FRI,
        t(18, 10),
        t(19, 30),
        genre=Genre.LATIN,
        about=(
            "Master percussionist Bill Summers is best known for his work\n"
            "with Herbie Hancock and the Headhunters, and with the Grammy-\n"
            "nominated Los Hombres Calientes. His jazz-salsa project Jazalsa\n"
            "is heavy on percussion and brass, drawing on decades at the\n"
            "forefront of Afro-Cuban jazz. Summers also contributed to the\n"
            "soundtracks of Roots, The Wiz, and The Color Purple with Quincy\n"
            "Jones. In New Orleans they call him Baba Bill, and his sets\n"
            "are guaranteed to move your feet."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.facebook.com/TheOfficialBillSummersFanPage/"],
    ),
    # ── Jazz Playhouse at the Royal Sonesta ───────────────────────────
    Act(
        "The Sam Lobley Band",
        JAZZPLAYHOUSE,
        FRI,
        t(11, 0),
        t(13, 30),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Bassist Sam Lobley grew up on Sinatra, Nat King Cole, and Louis\n"
            "Prima before diving deep into jazz and Black American Music at\n"
            "college. After moving to New Orleans, he immersed himself in the\n"
            "city's traditional jazz world, performing regularly at the Jazz\n"
            "Playhouse and appearing with Marty Peters and the Party Meters.\n"
            "Influenced by Ray Brown, Christian McBride, and Charles Mingus,\n"
            "Lobley leads a swinging combo well suited to the intimate Royal\n"
            "Sonesta room."
        ),
        about_source=AboutSource.RESEARCHED,
    ),
    Act(
        "Antoine Diel & New Orleans Misfit Power Band",
        JAZZPLAYHOUSE,
        FRI,
        t(14, 0),
        t(16, 30),
        genre=Genre.JAZZ_CONTEMPORARY,
        about=(
            "Antoine Diel is a Filipino-American vocalist who studied at\n"
            "USC's Thornton School of Music before making New Orleans his\n"
            "home. His captivating fusion of jazz, soul, and gospel reflects\n"
            "his diverse cultural background and the city's musical\n"
            "traditions. As bandleader of the Misfit Power Band and co-leader\n"
            "of the A2D2 Experience with Arsene DeLay, Diel brings polished\n"
            "vocal technique and infectious energy. He also teaches voice at\n"
            "Loyola University."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.antoinediel.com/"],
    ),
    Act(
        "Chucky C & Friends",
        JAZZPLAYHOUSE,
        FRI,
        t(17, 0),
        t(19, 30),
        genre=Genre.JAZZ_CONTEMPORARY,
        about=(
            "Charles Chucky C Elam III has earned the title The King of Feel\n"
            "Good through decades of electrifying performances. Trained under\n"
            "Johnny Fernandez, Ellis Marsalis, and Alvin Batiste, he plays\n"
            "tenor, alto, and soprano saxophone, flute, clarinet, harmonica,\n"
            "and piano. His Clearly Blue Band blends nightclub R&B with jazz\n"
            "and blues, pivoting seamlessly between genres. International\n"
            "highlights include the Umbrian Jazz Festival and the North Sea\n"
            "Jazz Festival."
        ),
        about_source=AboutSource.RESEARCHED,
    ),
    # ── French Market Traditional Jazz Stage ──────────────────────────
    Act(
        "Panorama Jazz Band",
        FRENCHMARKET,
        FRI,
        t(11, 30),
        t(13, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Clarinetist Ben Schenck founded the Panorama Jazz Band in 1996\n"
            "after moving from D.C. to New Orleans, inspired by Dr. Michael\n"
            "White's Young Tuxedo Jazz Band. This seven-piece acoustic\n"
            "ensemble interweaves classic New Orleans trad jazz with Jewish\n"
            "klezmer, Creole biguines from Martinique, South American folk,\n"
            "and other global party music. Hundreds of nightclub gigs,\n"
            "festivals, crawfish boils, and Mardi Gras parades later, they\n"
            "remain one of the city's most adventurous trad-jazz acts."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://panoramalandnola.com/"],
    ),
    Act(
        "Rickie Monie & the Traditional Jazz Ramblers",
        FRENCHMARKET,
        FRI,
        t(13, 30),
        t(15, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Pianist Rickie Monie has been a fixture at Preservation Hall\n"
            "since 1982, when he was called to substitute for the legendary\n"
            "Sweet Emma Barrett. Born in New Orleans in 1952, he played\n"
            "alongside masters like Percy Humphrey, Manny Sayles, and Dave\n"
            "Bartholomew. A National Medal of Arts recipient, Monie has\n"
            "dazzled audiences on five continents with his gospel-infused\n"
            "traditional jazz piano. The Ramblers carry that Preservation\n"
            "Hall spirit to the French Market stage."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://rickiemonie.com/"],
    ),
    Act(
        "The New Orleans Flairs",
        FRENCHMARKET,
        FRI,
        t(15, 30),
        t(17, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Led by fifth-generation clarinetist and saxophonist Louis Ford,\n"
            "The New Orleans Flairs perform big band favorites from the 1930s\n"
            "and 1940s alongside New Orleans traditional jazz standards. Ford\n"
            "is dedicated to the preservation of jazz, carrying on the legacy\n"
            "of his father Clarence Ford, who performed with Fats Domino for\n"
            "three decades. Their album Vintage Jazz includes classics like\n"
            "When The Saints Go Marching In and West End Blues."
        ),
        about_source=AboutSource.RESEARCHED,
    ),
    Act(
        "Ingrid Lucia",
        FRENCHMARKET,
        FRI,
        t(17, 30),
        t(19, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Born into a family of street musicians, Ingrid Lucia sang in\n"
            "her family's Flying Neutrinos band from the age of eight and\n"
            "honed her jazz vocal chops in New York alongside Tony Bennett.\n"
            "Her silky voice has drawn comparisons to Billie Holiday, and\n"
            "she brings a glamorous cabaret energy to trad jazz, blues, and\n"
            "originals. She also leads the New Orleans Nightingales, a\n"
            "rotating ensemble of twenty local female vocalists. A beloved\n"
            "New Orleans native with decades of stage magic."
        ),
        about_source=AboutSource.RESEARCHED,
    ),
    # ── French Market Dutch Alley Stage ───────────────────────────────
    Act(
        "Tyler Twerk Thomson",
        DUTCHALLEY,
        FRI,
        t(11, 15),
        t(12, 30),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Tyler Twerk Thomson is a spectacular young bassist originally\n"
            "from Toronto who moved to New Orleans to join Marla Dixon's\n"
            "Shotgun Jazz Band. He released his debut album on Twerk-O-Phonic\n"
            "Records, a label he launched after restoring a 1930s Presto K8\n"
            "lathe. His collaborators include some of the most sought-after\n"
            "trad-jazz musicians in the city, including trumpeter Ben Polcer\n"
            "and trombonist Charlie Halloran. Deep-swinging traditional jazz\n"
            "with DIY spirit."
        ),
        about_source=AboutSource.RESEARCHED,
    ),
    Act(
        "Palmetto Bug Stompers",
        DUTCHALLEY,
        FRI,
        t(12, 45),
        t(14, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Led by Washboard Chaz Leary on washboard and vocals, the\n"
            "Palmetto Bug Stompers are some of the city's most talented\n"
            "purveyors of traditional New Orleans jazz and country blues.\n"
            "Formed in the mid-2000s as a street band, they graduated from\n"
            "the Old Point Bar in Algiers to Jazz Fest, French Quarter Fest,\n"
            "and Lincoln Center's Mid Summer Night Swing. A favorite of\n"
            "Lindy Hop dancers, the Bugs bring impeccable musicianship and\n"
            "an infectious good time."
        ),
        about_source=AboutSource.RESEARCHED,
    ),
    Act(
        "The Pfister Sisters",
        DUTCHALLEY,
        FRI,
        t(14, 15),
        t(15, 30),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Since 1979, the Pfister Sisters have carried on the legacy of\n"
            "innovative jazz vocal harmony begun by New Orleans' own Boswell\n"
            "Sisters in the 1920s. The current lineup of Holley Bendtsen,\n"
            "Yvette Voelker, Karen Stoehr, and Amasa Miller delivers three-\n"
            "part harmony in venues from barrooms and Jazz at Lincoln Center\n"
            "to the Ascona Jazz Festival. They played themselves in an\n"
            "episode of HBO's Treme and have shared stages with Linda\n"
            "Ronstadt and Dr. John."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://pfistersisters.com/"],
    ),
    Act(
        "New Orleans Classic Jazz Orchestra",
        DUTCHALLEY,
        FRI,
        t(15, 45),
        t(17, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "The New Orleans Classic Jazz Orchestra is a large ensemble\n"
            "dedicated to performing and preserving the classic jazz\n"
            "repertoire of the Crescent City. Drawing from the tradition\n"
            "of big bands and early jazz orchestras, the group brings\n"
            "sophisticated arrangements and swinging energy to music that\n"
            "spans the genre's golden era. A French Quarter Fest regular,\n"
            "they are a perfect fit for the Dutch Alley stage's commitment\n"
            "to traditional jazz."
        ),
        about_source=AboutSource.GENERATED,
    ),
    # ── House of Blues Voodoo Garden Stage ─────────────────────────────
    Act(
        "Shawan Rice Trio",
        HOUSEOFBLUES,
        FRI,
        t(11, 15),
        t(12, 30),
        genre=Genre.RNB_SOUL,
        about=(
            "Vocalist Shawan Rice relocated from Harrisburg, Pennsylvania,\n"
            "to New Orleans in 2016 and quickly became a staple of the local\n"
            "scene. Her eclectic, rootsy neo-soul draws from Jimi Hendrix to\n"
            "Erykah Badu, and her 2023 EP Fever Dreams is her most polished\n"
            "release yet. She has appeared on major stages including Congo\n"
            "Square at Jazz Fest and Switzerland's Jazz Ascona Festival.\n"
            "In the intimate Voodoo Garden, her magnetic voice fills every\n"
            "corner."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://shawanmusic.com/"],
    ),
    Act(
        "Joey Houcke",
        HOUSEOFBLUES,
        FRI,
        t(12, 45),
        t(14, 45),
        genre=Genre.ROCK,
        about=(
            "The Joey Houck Band is a New Orleans act built on a\n"
            "conglomeration of rock, soul, and funky blues. From their home\n"
            "base in the Crescent City, they play regularly across Louisiana\n"
            "and the Gulf South with occasional touring runs up both coasts.\n"
            "A presence on the WWOZ live-music calendar and the local club\n"
            "circuit, Houck brings a raw, guitar-driven energy perfect for\n"
            "the Voodoo Garden's outdoor vibe."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.josephhouckmusic.com/"],
    ),
    Act(
        "Electric Ramble",
        HOUSEOFBLUES,
        FRI,
        t(15, 0),
        t(17, 0),
        genre=Genre.ROCK,
        about=(
            "Electric Ramble is a rock and soul band out of New Orleans that\n"
            "sits in the space between The Black Crowes, The Revivalists, and\n"
            "Marcus King. Vocalist Evan Hall, guitarist Brook Danos, bassist\n"
            "Tyler Self, and drummer William McMains deliver potent guitar\n"
            "riffs, compelling lyrics, and New Orleans rhythms that refuse\n"
            "to let you stand still. They secured their first major festival\n"
            "slot at the 2024 French Quarter Fest and have been building\n"
            "momentum ever since."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.electricramble.com/"],
    ),
    Act(
        "Borders Trio",
        HOUSEOFBLUES,
        FRI,
        t(17, 15),
        t(19, 15),
        genre=Genre.RNB_SOUL,
        about=(
            "Led by singer-songwriter Mia Borders, the Borders Trio brings\n"
            "a soul-drenched, genre-blending sound to the Voodoo Garden.\n"
            "Borders, a New Orleans native, mixes soul, funk, R&B, and\n"
            "electronic textures across a deep catalog that includes her\n"
            "2024 album Firewalker. She also runs Third Coast Entertainment,\n"
            "a booking agency elevating women, LGBTQ+, and BIPOC artists,\n"
            "and founded the Borders Foundation. A powerhouse vocalist with\n"
            "a community mission."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.miaborders.com/"],
    ),
    Act(
        "Tanglers",
        HOUSEOFBLUES,
        FRI,
        t(19, 30),
        t(21, 30),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "The Tanglers Bluegrass Band weave progressive bluegrass, folk,\n"
            "funk, and Americana into a toe-tapping fusion that captures both\n"
            "Appalachian and Crescent City energy. The five-piece lineup of\n"
            "Matt Rota on banjo, Graham Robinson on bass, Dylan Williams on\n"
            "mandolin, Jacob Tanner on dobro, and Craig Alexander on guitar\n"
            "has earned them a reputation as one of New Orleans' top\n"
            "bluegrass acts. Regular performers at Jazz Fest and local\n"
            "venues like The Howlin' Wolf and d.b.a."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://thetanglers.bandcamp.com/"],
    ),
]
