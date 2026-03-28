"""Thursday April 16, 2026 — FQF schedule data."""

from fqf.models import (
    ABITA,
    FISHFRY,
    HOUSEOFBLUES,
    JACKDANIELS,
    NEWORLEANS,
    PANAMLIFE,
    THU,
    TROPICAL,
    WILLOW,
    AboutSource,
    Act,
    Genre,
    t,
)

THURSDAY_ACTS: list[Act] = [
    # ── Abita Beer Stage ──────────────────────────────────────────────
    Act(
        "Seguenon Kone featuring Ivorie Spectacle",
        ABITA,
        THU,
        t(11, 30),
        t(12, 30),
        genre=Genre.WORLD,
        about=(
            "Master percussionist Seguenon Kone grew up in Ivory Coast playing balafon and\n"
            "djembe from the age of four, eventually touring with the National Ballet of the\n"
            "Ivory Coast as a teenager. After settling in New Orleans in 2008, he became a\n"
            "respected educator and ambassador for the deep cultural links between West Africa\n"
            "and the Crescent City. His ensemble Ivorie Spectacle is a drum-and-dance\n"
            "celebration of Ivorian music, costume, and rhythm that will get the whole crowd\n"
            "on their feet."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[
            "https://nolajazzmuseum.org/events/2022/12/15/"
            "the-new-orleans-jazz-museum-and-jazz-national-historical-park-"
            "presents-the-kone-residency-show"
        ],
    ),
    Act(
        "The Quickening",
        ABITA,
        THU,
        t(12, 50),
        t(13, 50),
        genre=Genre.MIXED_ECLECTIC,
        about=(
            "The Quickening formed in 2012 after frontman Blake Quick left local funk band\n"
            "Flow Tribe, and the group has been a staple of the New Orleans jam scene ever\n"
            "since. Vocalist Rachel 'Mama Ray' Murray shares lead duties with Quick, and\n"
            "their chemistry drives a sound soaked in soul, exploratory jamming, and\n"
            "Grateful Dead storytelling. A rotating cast of horns, pedal steel, and strings\n"
            "keeps every show unpredictable and dance-floor ready."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[
            "https://thequickeningmusic.bandcamp.com/",
            "https://www.instagram.com/thequickeningmusic/",
        ],
    ),
    Act(
        "Kermit Ruffins & the Barbecue Swingers",
        ABITA,
        THU,
        t(14, 10),
        t(15, 10),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Kermit Ruffins is a New Orleans institution: trumpeter, singer, and co-founder\n"
            "of the Rebirth Brass Band who has been spreading joy and Louis Armstrong-\n"
            "inspired horn work since the 1980s. His Barbecue Swingers, formed in 1992, are\n"
            "the perfect festival act -- tight traditional jazz with a party vibe, and Kermit\n"
            "himself might fire up the grill right on stage. Catch him if you want a genuine\n"
            "taste of New Orleans in every sense of the word."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[
            "https://www.kermitslounge.com/",
            "https://www.basinstreetrecords.com/artists/kermit-ruffins/",
        ],
    ),
    Act(
        "Big Chief Juan Pardo's Tribal Gold",
        ABITA,
        THU,
        t(15, 30),
        t(16, 30),
        genre=Genre.INDIAN_MARDI_GRAS,
        about=(
            "Big Chief Juan Pardo of the Golden Comanche tribe was born into the Black\n"
            "Masking Indian tradition and has been masking for over 20 years. Tribal Gold\n"
            "merges the Golden Comanche's chanting and tambourine-driven rhythms with the\n"
            "funky firepower of members of the New Orleans Suspects, creating a sound that\n"
            "crosses boundaries while honoring deep cultural roots. Pardo is also a published\n"
            "author and visual artist, making this one of the most multidimensional acts on\n"
            "the schedule."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[
            "https://ellanola.org/ellanotes/"
            "big-chief-juan-pardo-born-into-the-tradition-and-bringing-it-forward",
            "https://ragman.org/tribal-gold",
        ],
    ),
    Act(
        "Erica Falls & Vintage Soul",
        ABITA,
        THU,
        t(16, 50),
        t(18, 10),
        genre=Genre.RNB_SOUL,
        about=(
            "Erica Falls grew up in the 9th Ward steeped in the music of Aretha Franklin\n"
            "and Nina Simone, and she has carried that torch into a powerhouse career of her\n"
            "own. After five years as the featured vocalist with Galactic, she launched her\n"
            "solo project with the acclaimed album Homegrown. Multiple Offbeat Best Female\n"
            "Vocalist awards and collaborations with Allen Toussaint, Dr. John, and Sting\n"
            "speak to her standing. Her band Vintage Soul delivers exactly what the name\n"
            "promises -- timeless R&B that never left."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.ericafalls.com/"],
    ),
    Act(
        "The Soul Rebels",
        ABITA,
        THU,
        t(18, 40),
        t(20, 0),
        genre=Genre.BRASS_BAND,
        about=(
            "The Soul Rebels are an eight-piece brass powerhouse that fuse New Orleans\n"
            "second-line tradition with funk, hip-hop, and pop. Percussionists Derrick Moss\n"
            "and Lumar LeBlanc started the group out of Harold Dejan's Young Olympia Brass\n"
            "Band, and Cyril Neville gave them their name at a Tipitina's gig. Since then\n"
            "they have landed on NPR's Tiny Desk, The Late Show with Stephen Colbert, and\n"
            "scored music for Disney's Haunted Mansion. Their late-afternoon set is the\n"
            "perfect send-off for Thursday's festival crowd."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://thesoulrebels.com/"],
    ),
    # ── NewOrleans.com Stage ──────────────────────────────────────────
    Act(
        "Preservation Brass",
        NEWORLEANS,
        THU,
        t(11, 15),
        t(12, 25),
        genre=Genre.BRASS_BAND,
        about=(
            "The resident brass band of Preservation Hall, New Orleans' most treasured jazz\n"
            "venue, Preservation Brass carries on the lineage of Dejan's Olympia Brass Band.\n"
            "Led by trumpeters Mark Braud and Kevin Louis, the group earned a 2025 Grammy\n"
            "nomination for Best Regional Roots Music Album with their record For Fat Man.\n"
            "Hearing them outside the intimate Hall setting lets you appreciate the full\n"
            "power of their horn section in the open air."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.preservationhall.com/people/preservation-brass/"],
    ),
    Act(
        "Banu Gibson",
        NEWORLEANS,
        THU,
        t(12, 45),
        t(14, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Banu Gibson is one of the few contemporary vocalists devoted exclusively to the\n"
            "songs of the 1920s, 30s, and 40s. A singer, bandleader, dancer, and banjoist,\n"
            "she moved to New Orleans in 1973 and founded her Hot Jazz Orchestra in 1981.\n"
            "The ensemble has played with symphony orchestras from the Boston Pops to San\n"
            "Diego, and Gibson also runs the New Orleans Trad Jazz Camp. Her swinging stage\n"
            "presence makes her a perennial FQF favorite."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["http://www.banugibson.com/"],
    ),
    Act(
        "Mahogany Hall All Stars Band",
        NEWORLEANS,
        THU,
        t(14, 20),
        t(15, 30),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Named for the Mahogany Jazz Hall in the Marigny, this all-star ensemble is led\n"
            "by clarinetist and educator Tom Fischer and features veteran musicians who bring\n"
            "decades of experience to every performance. The five-piece group keeps the\n"
            "flame of traditional New Orleans jazz burning bright with tight arrangements\n"
            "and an easy, swinging feel that sounds right at home on a French Quarter stage."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.wwoz.org/organizations/mahogany-jazz-hall"],
    ),
    Act(
        "Leroy Jones & New Orleans' Finest",
        NEWORLEANS,
        THU,
        t(15, 50),
        t(17, 10),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Trumpeter Leroy Jones has embodied the spirit of traditional New Orleans jazz\n"
            "for over fifty years. He was leading the Fairview Baptist Church Marching Band\n"
            "at age 12, went on to join Harry Connick Jr.'s big band, and earned a place in\n"
            "the New Orleans Jazz Hall of Fame. With his group New Orleans' Finest, he\n"
            "delivers the real deal: warm tone, impeccable swing, and a direct line back to\n"
            "the earliest days of jazz in this city."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.preservationhall.com/people/leroy-jones/"],
    ),
    Act(
        "The Lilli Lewis Project",
        NEWORLEANS,
        THU,
        t(17, 30),
        t(18, 45),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "Lilli Lewis is a classically trained opera singer and pianist who reinvented\n"
            "herself as the 'Folk Rock Diva' after moving to New Orleans. Backed by a big\n"
            "band of top local musicians, the Lilli Lewis Project blends folk, rock, soul,\n"
            "and jazz into something uniquely personal. Her album Americana landed on NPR\n"
            "Music's Top 10 Albums of the Week, and her rich mezzo-soprano voice fills every\n"
            "corner of whatever stage she takes."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[
            "https://www.lillilewis.com/2022/",
            "https://lillilewisproject.com/",
        ],
    ),
    # ── Tropical Isle Hand Grenade Stage ──────────────────────────────
    Act(
        "Mem Shannon & The Membership",
        TROPICAL,
        THU,
        t(11, 10),
        t(12, 10),
        genre=Genre.BLUES,
        about=(
            "Mem Shannon is a New Orleans bluesman with one of the great origin stories:\n"
            "a cab driver who put his music career on hold after his father's death, then\n"
            "returned to the stage in 1990 at the urging of a former bandmate. His debut,\n"
            "A Cab Driver's Blues, earned critical acclaim, and his song S.U.V. won Living\n"
            "Blues magazine's Critics Poll Song of the Year. Shannon and The Membership\n"
            "deliver gritty, original New Orleans blues with a storyteller's touch."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.memshannon.com/"],
    ),
    Act(
        "Sir Chantz Powell & The Sound Of Funk (S.O.F.)",
        TROPICAL,
        THU,
        t(12, 30),
        t(13, 30),
        genre=Genre.FUNK,
        about=(
            "Sir Chantz Powell is a singer, trumpeter, dancer, and actor who signed with\n"
            "Decca/Universal at age 16 and has headlined stages from the Royal Albert Hall\n"
            "to the North Sea Jazz Festival. A true New Orleans multi-talent, he brings a\n"
            "high-energy show rooted in funk and soul that draws on the city's brass\n"
            "tradition while pushing it into contemporary territory. His band The Sound Of\n"
            "Funk keeps the groove tight and the audience moving."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[
            "https://www.chantz.com/home/",
            "https://playingforchange.com/artists/chantz-powell",
        ],
    ),
    Act(
        "Susan Cowsill",
        TROPICAL,
        THU,
        t(13, 50),
        t(14, 50),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "Susan Cowsill rose to fame as the youngest member of the 1960s family band\n"
            "The Cowsills, singing on their number-one hit Hair as a child. She relocated\n"
            "to New Orleans in 1993 and built a second career as a folk-rock songwriter,\n"
            "joining the Continental Drifters and later going solo. Rolling Stone called\n"
            "her album Lighthouse 'an earthy, often crunchy folk-rock gem.' Her lived-in\n"
            "voice and warm stage presence make her a natural fit for an afternoon set."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://susancowsillband.bandcamp.com/"],
    ),
    Act(
        "Yusa & Mahmoud Chouki",
        TROPICAL,
        THU,
        t(15, 10),
        t(16, 10),
        genre=Genre.WORLD,
        about=(
            "This pairing brings together two globe-spanning musical voices. Yusa is a\n"
            "Cuban singer-songwriter from the Buena Vista district of Havana, known as a\n"
            "top ambassador for 21st-century Cuban music and a former musical director of\n"
            "the band Interactivo. Mahmoud Chouki is a Moroccan-born master guitarist now\n"
            "based in New Orleans whose art bridges European classical, Andalusian, and\n"
            "Latin American traditions. Together they weave an irresistible cross-cultural\n"
            "conversation that could only happen in a city like New Orleans."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[
            "https://en.wikipedia.org/wiki/Yusa",
            "https://www.frenchquarterjournal.com/archives/the-magic-of-mahmoud-chouki",
        ],
    ),
    Act(
        "Royal Essence",
        TROPICAL,
        THU,
        t(16, 30),
        t(17, 45),
        genre=Genre.RNB_SOUL,
        about=(
            "Royal Essence is a New Orleans show band made up of veteran musicians and\n"
            "powerhouse vocalists. They serve as the house band for the Zulu Social Aid\n"
            "and Pleasure Club, performing at Lundi Gras and Mardi Gras balls year after\n"
            "year. Their repertoire spans classic R&B, blues, pop, and dance music, with\n"
            "influences from Ray Charles to Stevie Wonder. Expect polished choreography,\n"
            "tight horn arrangements, and that unmistakable Big Easy party energy."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://royalessenceshowband.com/"],
    ),
    Act(
        "Bag of Donuts",
        TROPICAL,
        THU,
        t(18, 15),
        t(19, 45),
        genre=Genre.ROCK,
        about=(
            "Four-time Offbeat Cover Band of the Year and the first cover band inducted\n"
            "into the Louisiana Music Hall of Fame, Bag of Donuts has been a New Orleans\n"
            "party institution since 1988. The six-piece group plays what they call\n"
            "Superpop -- hits from every era delivered with kabuki makeup, wild costumes,\n"
            "and boundless energy. They were the first cover band to play Jazz Fest and\n"
            "the first to sell out House of Blues. Closing out the Tropical Isle stage on\n"
            "Thursday, they are guaranteed to leave the crowd grinning."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://bagofdonuts.com/"],
    ),
    # ── Jack Daniel's Stage ───────────────────────────────────────────
    Act(
        "R & R Smokin' Foundation",
        JACKDANIELS,
        THU,
        t(11, 10),
        t(12, 30),
        genre=Genre.FUNK,
        about=(
            "R & R Smokin' Foundation is a New Orleans funk outfit that brings a heavy\n"
            "groove to the local festival circuit. Rooted in the city's deep funk tradition,\n"
            "the band layers tight horn lines over driving rhythms to get crowds moving\n"
            "early in the day. They are a welcome addition to the Jack Daniel's Stage\n"
            "lineup, setting the tone for a stacked Thursday bill."
        ),
        about_source=AboutSource.GENERATED,
    ),
    Act(
        "Bon Bon Vivant",
        JACKDANIELS,
        THU,
        t(12, 50),
        t(13, 50),
        genre=Genre.ROCK,
        about=(
            "Bon Bon Vivant is a New Orleans indie band helmed by songwriter and front-\n"
            "woman Abigail Cosio, saxophonist Jeremy Kelley, and sister-harmony vocalist\n"
            "Glori Cosio. Their sound blends bawdy cabaret, dark ballads, and uptempo\n"
            "indie dance rock -- think Amy Winehouse meets Florence and the Machine with\n"
            "a New Orleans twist. Offbeat named them Best Emerging Artist of 2018, and\n"
            "their Jazz Fest debut in 2022 cemented their arrival on the big stage."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.bonbonvivantmusic.com/"],
    ),
    Act(
        "Juice",
        JACKDANIELS,
        THU,
        t(14, 10),
        t(15, 10),
        genre=Genre.FUNK,
        about=(
            "Founded by bassist and vocalist Dave Jordan at LSU in 1996, Juice exploded\n"
            "onto the New Orleans scene in 1998 and quickly became one of the city's premier\n"
            "touring funk acts. At their peak they averaged 160 shows a year, earning the\n"
            "Offbeat Best Emerging Funk/Soul/R&B Band award in 2000. Their creative mix of\n"
            "New Orleans funk, blues, second line, and rock keeps the dance floor packed\n"
            "from the first note."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.nolajuicemusic.com/"],
    ),
    Act(
        "Sierra Green and the Giants",
        JACKDANIELS,
        THU,
        t(15, 30),
        t(16, 40),
        genre=Genre.RNB_SOUL,
        about=(
            "Sierra Green grew up in the 7th Ward singing in church, then learned to\n"
            "command an audience by busking on Frenchmen Street. Before long she graduated\n"
            "to packed club residencies and became known as the Queen of Frenchmen Street.\n"
            "Her band the Giants -- bassist Miguel Perez, guitarist Paul Provosty, and a\n"
            "full horn section -- backs her on soulful originals that live at the crossroads\n"
            "of soul, blues, and R&B. Their album Here We Are is proof this crew has arrived."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://sierragreenandthegiants.com/"],
    ),
    Act(
        "Rebirth Brass Band",
        JACKDANIELS,
        THU,
        t(17, 0),
        t(18, 20),
        genre=Genre.BRASS_BAND,
        about=(
            "Rebirth Brass Band has been a cornerstone of New Orleans music since 1983,\n"
            "when Philip and Keith Frazier, Kermit Ruffins, and friends from Treme launched\n"
            "the group at Clark Senior High School. Grammy winners for Rebirth of New\n"
            "Orleans, they fuse traditional second-line brass with funk, hip-hop, and soul\n"
            "in a way that is simultaneously reverent and revolutionary. If you see one\n"
            "brass band at the festival, make it this one."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://rebirthbrassband.com/"],
    ),
    Act(
        "Bobby Rush",
        JACKDANIELS,
        THU,
        t(18, 50),
        t(20, 0),
        genre=Genre.BLUES,
        about=(
            "Three-time Grammy winner, Blues Hall of Famer, and self-proclaimed King of the\n"
            "Chitlin' Circuit, Bobby Rush has been performing for over six decades. Born in\n"
            "Homer, Louisiana, he honed his craft alongside Muddy Waters and Little Walter\n"
            "in Chicago before developing a style he calls 'folk funk' -- deeply rooted yet\n"
            "decidedly modern. At 92, his live show remains one of the most colorful and\n"
            "energetic in the blues world. Do not miss this legend."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.bobbyrushbluesman.com/"],
    ),
    # ── Willow Dispensary Stage ───────────────────────────────────────
    Act(
        "T'Monde",
        WILLOW,
        THU,
        t(11, 10),
        t(12, 20),
        genre=Genre.CAJUN,
        about=(
            "T'Monde -- Cajun French for 'little people' or 'little world' -- features\n"
            "three accomplished young musicians with a combined ten Grammy nominations.\n"
            "Drew Simon, Megan Brown, and Kellii Jones play old-fashioned Cajun music\n"
            "ranging from rocking two-steps to sorrowful waltzes, drawing on influences\n"
            "from early country to ancient French and Creole ballads. Offbeat calls them\n"
            "'a creative fusion of classic country and out-of-the-way Cajun.' The perfect\n"
            "way to kick off the Willow stage's Cajun and zydeco Thursday."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["http://www.tmonde.com/"],
    ),
    Act(
        "Gerard Delafose and The Zydeco Gators",
        WILLOW,
        THU,
        t(12, 40),
        t(13, 50),
        genre=Genre.ZYDECO,
        about=(
            "Gerard Delafose comes from zydeco royalty: his grandfather John Delafose was\n"
            "a legend, and his uncle Geno carries the family banner forward. Gerard has been\n"
            "performing since age four and formed the Zydeco Gators in 2007. A Grammy-\n"
            "nominated international touring act, the band plays over 100 shows a year,\n"
            "from Jazz Fest to Switzerland's Blues to Bop festival. Expect hard-driving\n"
            "accordion and washboard grooves that will have you two-stepping in the grass."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://gerarddelafose.com/"],
    ),
    Act(
        "Waylon Thibodeaux Band",
        WILLOW,
        THU,
        t(14, 10),
        t(15, 10),
        genre=Genre.CAJUN,
        about=(
            "Dubbed 'Louisiana's Rockin' Fiddler,' Waylon Thibodeaux has been performing\n"
            "professionally since age 13 and won the state fiddle championship at 16. A\n"
            "Houma native from bayou country, his sound is a gumbo of Cajun, zydeco, swamp\n"
            "pop, and a little rock and roll. He is a Louisiana Music Hall of Famer who has\n"
            "played throughout the US, Canada, France, and Central and South America. Over\n"
            "40 years in, his energy on stage has not dimmed one bit."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.waylont.com/"],
    ),
    Act(
        "Nathan and the Zydeco Cha Chas",
        WILLOW,
        THU,
        t(15, 30),
        t(16, 40),
        genre=Genre.ZYDECO,
        about=(
            "Nathan Williams Sr. grew up in a French Creole-speaking home in St. Martinville\n"
            "and founded his band in 1985 after a recommendation from Buckwheat Zydeco\n"
            "landed him a deal with Rounder Records. For nearly four decades the Zydeco\n"
            "Cha Chas have packed dance floors from his brother's convenience store in\n"
            "Lafayette to Lincoln Center and the Grand Ole Opry. Their 2023 Grammy\n"
            "nomination for Lucky Man confirmed what fans already knew: Nathan is the real\n"
            "deal."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://zydecochachas.com/"],
    ),
    Act(
        "Amanda Shaw",
        WILLOW,
        THU,
        t(17, 0),
        t(18, 10),
        genre=Genre.CAJUN,
        about=(
            "Amanda Shaw picked up a violin at age four and became the youngest soloist\n"
            "ever to appear with the Baton Rouge Symphony at seven. A Mandeville native\n"
            "raised on fais do-dos and New Orleans funk alike, she signed with Rounder\n"
            "Records at 15 and has since appeared on Dick Clark's New Year's Rockin' Eve\n"
            "and the Macy's Thanksgiving Day Parade. A Louisiana Music Hall of Famer with\n"
            "nine releases and counting, she brings a joyful, fiddle-driven energy that\n"
            "bridges Cajun tradition and modern showmanship."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://amandashaw.com/"],
    ),
    Act(
        "Johnny Sketch and the Dirty Notes",
        WILLOW,
        THU,
        t(18, 45),
        t(20, 0),
        genre=Genre.FUNK,
        about=(
            "Johnny Sketch and the Dirty Notes formed in 2001 to win a Loyola University\n"
            "battle of the bands and never stopped. Classically and jazz-trained, the\n"
            "six-piece -- keys, sax, trumpet, guitar, bass, and drums -- creates music\n"
            "that is analytically interesting and impossibly danceable. Their carefully\n"
            "crafted live show blends jazz, blues, funk, and rock, and has earned them a\n"
            "devoted national following. Closing out the Willow stage Thursday night, they\n"
            "will leave nothing on the table."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.johnnysketch.com/"],
    ),
    # ── Louisiana Fish Fry Stage ──────────────────────────────────────
    Act(
        "Red Hot Brass Band",
        FISHFRY,
        THU,
        t(11, 10),
        t(12, 30),
        genre=Genre.BRASS_BAND,
        about=(
            "The Red Hot Brass Band started in 2006 under the mentorship of revered groups\n"
            "like the Storyville Stompers and the Treme Brass Band. Dedicated to preserving\n"
            "the traditions that accompany the jazz culture of New Orleans, they play a\n"
            "straight-ahead traditional brass sound that sets the right mood for a day of\n"
            "music on the Louisiana Fish Fry Stage."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://frenchquarterfest.org/artists/red-hot-brass-band/"],
    ),
    Act(
        "504 Millz",
        FISHFRY,
        THU,
        t(12, 35),
        t(13, 5),
        genre=Genre.ELECTRONIC_DJ,
        about=(
            "504 Millz is a New Orleans-based producer and DJ who specializes in bounce\n"
            "music, the high-energy call-and-response style born in the city's housing\n"
            "projects. Known for fiery remixes and original productions, 504 Millz keeps\n"
            "the party going with bass-heavy beats and Mardi Gras Indian-influenced\n"
            "rhythms that are impossible to stand still to."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://soundcloud.com/killa-millz"],
    ),
    Act(
        "J.A.M. Brass Band",
        FISHFRY,
        THU,
        t(13, 10),
        t(14, 30),
        genre=Genre.BRASS_BAND,
        about=(
            "J.A.M. Brass Band is a tight, exciting ensemble on the New Orleans brass\n"
            "band scene. Known for clean musicianship and an energetic sound, they hold\n"
            "down regular gigs at Balcony Music Club and have become a familiar presence\n"
            "at local festivals. Their set on the Fish Fry Stage is a chance to catch a\n"
            "rising group keeping the brass tradition fresh."
        ),
        about_source=AboutSource.RESEARCHED,
    ),
    Act(
        "Zeus",
        FISHFRY,
        THU,
        t(14, 35),
        t(15, 15),
        genre=Genre.ELECTRONIC_DJ,
        about=(
            "Zeus is a New Orleans-based artist on the local bounce and hip-hop scene.\n"
            "Performing on the Louisiana Fish Fry Stage alongside brass bands and DJs,\n"
            "Zeus brings high-energy beats and crowd-moving rhythms that fit right into\n"
            "the stage's mix of brass and DJ talent."
        ),
        about_source=AboutSource.GENERATED,
    ),
    Act(
        "SOUL Brass Band",
        FISHFRY,
        THU,
        t(15, 20),
        t(16, 40),
        genre=Genre.BRASS_BAND,
        about=(
            "SOUL Brass Band is the brainchild of percussionist Derrick 'Smoker' Freeman,\n"
            "Billboard-charting saxophonist James Martin, and Grammy-winning trombonist\n"
            "Miles Lyons. The ensemble bridges classic brass band tradition with contemporary\n"
            "funk, hip-hop, and soul, capturing the sound and spirit of modern New Orleans.\n"
            "Known for electrifying performances at Jazz Fest and French Quarter Fest, they\n"
            "are expanding the legacy of New Orleans brass for audiences worldwide."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://soulbrassband.com/"],
    ),
    Act(
        "DJ Legatron Prime",
        FISHFRY,
        THU,
        t(16, 45),
        t(17, 30),
        genre=Genre.ELECTRONIC_DJ,
        about=(
            "DJ Legatron Prime -- born Sage Edgerson -- is a New Orleans native and multi-\n"
            "genre DJ who has been a force in the city's nightlife since 2015. She holds\n"
            "down a Saturday headliner slot at The Dragons Den with her weekly PRIMETIME\n"
            "party and co-curates Where My Girls At? NOLA, the city's only monthly women's\n"
            "party. Featured on Boiler Room, nominated for Offbeat Best DJ, and recognized\n"
            "in Gambit's 40 Under 40, she spins Black girl magic across every genre."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.legatronprime.com/"],
    ),
    Act(
        "New Orleans Nightcrawlers",
        FISHFRY,
        THU,
        t(17, 35),
        t(18, 55),
        genre=Genre.BRASS_BAND,
        about=(
            "The Nightcrawlers are a funky, rootsy brass band supergroup that took home the\n"
            "2021 Grammy for Best Regional Roots Music Album with Atmosphere and earned a\n"
            "second nomination for Too Much to Hold. Founded in 1994 by Tom McDermott, Matt\n"
            "Perrine, and Kevin Clark as a writers' workshop for brass band music, the group\n"
            "stood apart from day one with clever songwriting and Latin-tinged arrangements.\n"
            "Their set is one of Thursday's can't-miss performances."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://neworleansnightcrawlersbrassband.com/"],
    ),
    Act(
        "Raj Smoove",
        FISHFRY,
        THU,
        t(19, 0),
        t(20, 0),
        genre=Genre.ELECTRONIC_DJ,
        about=(
            "New Orleans Saints game-day DJ, Lil Wayne-endorsed 'greatest DJ in the world,'\n"
            "and board member of French Quarter Festivals Inc., Raj Smoove has been rocking\n"
            "crowds for over 30 years. He got his first paid gig at 14, and has since\n"
            "collaborated with Juvenile, Mannie Fresh, PJ Morton, and Tank Ball. A member\n"
            "of the Recording Academy with deep roots in the city's hip-hop scene, he\n"
            "closes out Thursday's Fish Fry Stage in style."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["http://rajsmoove.com/"],
    ),
    # ── Pan-American Life Insurance Group Stage ───────────────────────
    Act(
        "Gal Holiday and the Honky Tonk Revue",
        PANAMLIFE,
        THU,
        t(11, 0),
        t(12, 10),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "Gal Holiday and the Honky Tonk Revue have been at the vanguard of New Orleans'\n"
            "country scene since forming in 2004. Fronted by Appalachian-born vocalist\n"
            "Vanessa Niemann -- sometimes called the Punk Rock Patsy Cline -- the band\n"
            "delivers Americana, country, and rockabilly with infectious dance-hall energy.\n"
            "They have shared the stage with Willie Nelson, Marcia Ball, and the Blind Boys\n"
            "of Alabama, and are staples at Jazz Fest and other major events."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.galholiday.com/"],
    ),
    Act(
        "The Tin Men",
        PANAMLIFE,
        THU,
        t(12, 30),
        t(13, 30),
        genre=Genre.MIXED_ECLECTIC,
        about=(
            "The Tin Men are America's premier sousaphone, washboard, and guitar trio.\n"
            "Washboard Chaz Leary, songwriter Alex McMurray, and Grammy-winning sousaphonist\n"
            "Matt Perrine have been performing together since 2002, exploring an eclectic\n"
            "array of American pop from jug band swing to Motown to easy listening. Offbeat\n"
            "called them 'one of the most interesting bands to emerge from New Orleans in\n"
            "years.' An only-in-New-Orleans act that should not be missed."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.tinmenmusic.com/"],
    ),
    Act(
        "T-Ray & The Trendsetters",
        PANAMLIFE,
        THU,
        t(13, 50),
        t(14, 50),
        genre=Genre.RNB_SOUL,
        about=(
            "T-Ray the Violinist is an eclectic fusion artist who has refused to let the\n"
            "classical context of his instrument define him. Based in New Orleans, he has\n"
            "opened for Grammy winners like Frankie Beverly & Maze and Anthony Hamilton,\n"
            "and collaborated with Big Freedia and Tank and the Bangas. With his band\n"
            "The Trendsetters, he delivers a genre-bending live show that blends R&B, funk,\n"
            "and soul through the lens of his electric violin."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.traytheviolinist.com/"],
    ),
    Act(
        "Muévelo",
        PANAMLIFE,
        THU,
        t(15, 10),
        t(16, 10),
        genre=Genre.LATIN,
        about=(
            "Muévelo -- Spanish for 'Move it!' -- started as a one-off Celia Cruz tribute\n"
            "and quickly became one of New Orleans' favorite Latin dance bands. Led by\n"
            "singer Margie Perez and Grammy-winning saxophonist Brent Rose, the ten-piece\n"
            "ensemble blends Cuban son, salsa, and tropical rhythms with the soulful essence\n"
            "of the Crescent City. They hold a monthly La Noche Caliente residency and have\n"
            "ignited dance floors at Jazz Fest, French Quarter Fest, and Bayou Boogaloo."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.wwoz.org/acts/muevelo"],
    ),
    Act(
        "John Mooney",
        PANAMLIFE,
        THU,
        t(16, 30),
        t(17, 50),
        genre=Genre.BLUES,
        about=(
            "John Mooney has spent nearly five decades developing a singular style that\n"
            "fuses Delta blues slide guitar with the funky second-line beat of New Orleans.\n"
            "Mentored as a teenager by the great Son House, he moved to New Orleans in 1976\n"
            "and immersed himself in the R&B scene alongside Earl King, the Meters, and\n"
            "Professor Longhair. His group Bluesiana has been his vehicle since 1981,\n"
            "touring the US, Europe, Australia, and Japan. A masterclass in where the\n"
            "Delta meets the Crescent City."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://intrepidartists.com/artists/john-mooney/"],
    ),
    Act(
        "The New Orleans Klezmer All Stars",
        PANAMLIFE,
        THU,
        t(18, 10),
        t(19, 30),
        genre=Genre.WORLD,
        about=(
            "Since 1991, the New Orleans Klezmer All Stars have been melding the Jewish\n"
            "folk music of eastern Europe with early jazz, funk, and Dixieland. Led by\n"
            "accordionist Glenn Hartman, Galactic's Ben Ellman on sax, and guitarist\n"
            "Jonathan Freilich, the band's rhythm section has included Mean Willie Green of\n"
            "the Neville Brothers and Galactic's Stanton Moore. The result is energetic,\n"
            "aggressive, and often hilarious -- a musical conversation that could only\n"
            "happen in New Orleans."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.klezmerallstars.com/"],
    ),
    # ── House of Blues Voodoo Garden Stage ─────────────────────────────
    Act(
        "Jake Landry",
        HOUSEOFBLUES,
        THU,
        t(12, 30),
        t(14, 30),
        genre=Genre.BLUES,
        about=(
            "Jake Landry is a singer-songwriter and multi-instrumentalist from South\n"
            "Louisiana who has become a fixture of the New Orleans club scene. A regular\n"
            "performer at the House of Blues, he serves up soulful vocals and sharp guitar\n"
            "work across an energetic mix of blues, jazz, R&B, and covers. Whether fronting\n"
            "a small combo or a full nine-piece band, Landry keeps the Voodoo Garden crowd\n"
            "locked in."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.instagram.com/jakelandrymusic/"],
    ),
    Act(
        "Funky Lampshades",
        HOUSEOFBLUES,
        THU,
        t(15, 0),
        t(17, 0),
        genre=Genre.FUNK,
        about=(
            "Funky Lampshades are a Gulf Coast-based band fronted by Austin Thompson that\n"
            "channels the spirits of classic R&B, rock, blues, and soul into a modern,\n"
            "high-energy show. While they hail from Gulf Shores, Alabama, they are frequent\n"
            "performers at New Orleans venues including the House of Blues. Their sly\n"
            "interpretations of funk and soul classics make them a natural fit for an\n"
            "afternoon set in the Voodoo Garden."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.instagram.com/funky.lampshades/"],
    ),
    Act(
        "Cary Hudson",
        HOUSEOFBLUES,
        THU,
        t(17, 30),
        t(19, 30),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "Cary Hudson is the guitarist, singer, and main songwriter behind the\n"
            "influential alt-country band Blue Mountain, which shared stages with Uncle\n"
            "Tupelo, Son Volt, and Wilco and graced the cover of No Depression magazine.\n"
            "A Mississippi native from Sumrall, he was named one of Gibson's Top 10 Alt-\n"
            "Country Guitarists of all time. Since Blue Mountain's final tour in 2013, his\n"
            "solo work continues to mine Southern roots, rock, and Americana with an honest,\n"
            "lived-in voice."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=[
            "http://caryhudson.com/",
            "https://caryhudson.bandcamp.com/",
        ],
    ),
    Act(
        "Julian Primeaux",
        HOUSEOFBLUES,
        THU,
        t(19, 30),
        t(21, 30),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "Grammy nominee and Louisiana Music Hall of Fame inductee Julian Primeaux grew\n"
            "up in the bayous of Lafayette and was performing live by age 12. His rock-n-\n"
            "soul and Southern roots sound has taken him from Louisiana juke joints to Times\n"
            "Square to concert halls across Europe. An NPR World Cafe spotlight artist, he\n"
            "brings guitar-driven storytelling soaked in the spirit of south Louisiana to\n"
            "the Voodoo Garden's closing set on Thursday."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.julianprimeaux.com/"],
    ),
]
