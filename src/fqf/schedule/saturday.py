"""Saturday April 18, 2026 — FQF schedule data.

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
    SAT,
    SCHOOLHOUSE,
    TROPICAL,
    WILLOW,
    AboutSource,
    Act,
    Genre,
    t,
)

SATURDAY_ACTS: list[Act] = [
    # ── Abita Beer Stage ──────────────────────────────────────────────
    Act(
        "Gregg Martinez & the Delta Kings",
        ABITA,
        SAT,
        t(11, 30),
        t(12, 30),
        genre=Genre.RNB_SOUL,
        about=(
            "Louisiana Music Hall of Fame inductee Gregg 'Mac Daddy' Martinez is a\n"
            "swamp pop and R&B crooner from Lafayette whose vocal style channels\n"
            "the golden-era soul of Sam Cooke, Marvin Gaye, and Al Green. With the\n"
            "Delta Kings backing him, he delivers a dance-floor set steeped in\n"
            "south Louisiana groove. His album Soul of the Bayou reached the top\n"
            "five on the national R&B chart."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.greggmartinez.com"],
    ),
    Act(
        "Ryan Batiste and Raw Revolution",
        ABITA,
        SAT,
        t(12, 50),
        t(13, 50),
        genre=Genre.RNB_SOUL,
        about=(
            "Ryan 'Shaggadelic' Batiste grew up in New Orleans' legendary Batiste\n"
            "musical family and channels that heritage into a high-energy blend of\n"
            "hip-hop, R&B, and electronic production. A multi-instrumentalist who\n"
            "moved from drums to keys to the mic, he leads Raw Revolution with a\n"
            "genre-crossing confidence honed since high school. Beyond performing,\n"
            "Ryan founded L.O.C.A.L.S' Fest and runs Project Revolution, a music\n"
            "education program for middle-schoolers."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.facebook.com/rdbatiste/"],
    ),
    Act(
        "Big Chief Monk Boudreaux and the Golden Eagles",
        ABITA,
        SAT,
        t(14, 10),
        t(15, 10),
        genre=Genre.INDIAN_MARDI_GRAS,
        about=(
            "Big Chief Monk Boudreaux has led the Golden Eagles Mardi Gras Indian\n"
            "tribe for over fifty years, making him one of the most revered figures\n"
            "in the Black masking tradition. A 2016 National Heritage Fellow and\n"
            "Grammy-nominated artist, he is a living embodiment of New Orleans'\n"
            "African diaspora culture. His electrifying stage presence and\n"
            "deep-rooted chants make every performance a spiritual event\n"
            "you do not want to miss."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://bigchiefmonkboudreaux.com/"],
    ),
    Act(
        "Dawn Richard",
        ABITA,
        SAT,
        t(15, 30),
        t(16, 30),
        genre=Genre.RNB_SOUL,
        about=(
            "Born in New Orleans' Lower Ninth Ward, Dawn Richard is a visionary\n"
            "singer, songwriter, and producer known for genre-defying artistry.\n"
            "From Danity Kane and Dirty Money to acclaimed solo albums like\n"
            "Second Line, she fuses R&B, electronic, and experimental sounds\n"
            "into boundary-pushing pop. Her father played in Chocolate Milk\n"
            "and that Crescent City DNA runs through everything she creates."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.mergerecords.com/artist/dawn_richard"],
    ),
    Act(
        "George Porter Jr & Runnin' Pardners",
        ABITA,
        SAT,
        t(17, 0),
        t(18, 20),
        genre=Genre.FUNK,
        about=(
            "George Porter Jr. is the bassist and co-founder of The Meters,\n"
            "the band widely recognized as progenitors of funk. Since 1990 he\n"
            "has led the Runnin' Pardners, a project that distills decades of\n"
            "New Orleans groove into tight, improvisational sets beloved on the\n"
            "festival and jam-band circuits. At any FQF, catching George lay\n"
            "down a bass line is practically a pilgrimage."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.georgeporterjr.com"],
    ),
    Act(
        "Flow Tribe",
        ABITA,
        SAT,
        t(18, 40),
        t(20, 0),
        genre=Genre.MIXED_ECLECTIC,
        about=(
            "Flow Tribe has been stirring up New Orleans since 2004 with a\n"
            "genre-spanning cocktail they call 'backbone-cracking music' \u2014 funk,\n"
            "rock, R&B, hip-hop, and Afro-Cuban rhythms all in one sweaty set.\n"
            "Formed by Brother Martin High School friends and forged by the\n"
            "post-Katrina return, the band celebrated twenty years running in\n"
            "2024. Their album BOSS, produced by Mannie Fresh, cracked the\n"
            "Billboard R&B chart."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.flowtribe.com"],
    ),
    # ── NewOrleans.com Stage ──────────────────────────────────────────
    Act(
        "Tim Laughlin",
        NEWORLEANS,
        SAT,
        t(11, 15),
        t(12, 35),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Tim Laughlin is often called the protege of Pete Fountain and is one\n"
            "of New Orleans' premier traditional jazz clarinetists. Born and raised\n"
            "in the city, he keeps the idiom fresh with original compositions \u2014\n"
            "he is the first New Orleans clarinetist to record an entire album of\n"
            "originals. During the pandemic he became beloved for daily 'balcony\n"
            "concerts' on Royal Street in the French Quarter."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["http://www.timlaughlin.com"],
    ),
    Act(
        "The Big Easy Boys",
        NEWORLEANS,
        SAT,
        t(12, 45),
        t(14, 0),
        genre=Genre.RNB_SOUL,
        about=(
            "The Big Easy Boys are a throwback quartet paying tribute to the\n"
            "twentieth-century greats of New Orleans R&B \u2014 Fats Domino, Allen\n"
            "Toussaint, Irma Thomas, Dr. John, and Louis Prima among them.\n"
            "Backed by a seven-piece band and the Big Easy Babes, their tight\n"
            "harmonies and choreography make for a feel-good revue that\n"
            "celebrates the city's rich musical heritage."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.bigeasyboys.com"],
    ),
    Act(
        "Wendell Brunious",
        NEWORLEANS,
        SAT,
        t(14, 20),
        t(15, 30),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Wendell Brunious comes from one of New Orleans' most storied Creole\n"
            "music families and carries more than 2,000 songs in his repertoire.\n"
            "He became leader of the Preservation Hall group after Kid Thomas\n"
            "Valentine's passing in 1987 and in 2023 was named Preservation\n"
            "Hall's first-ever musical director. His smooth trumpet tone and deep\n"
            "ballad interpretations are the sound of the city's living tradition."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.preservationhall.com/people/wendell-brunious/"],
    ),
    Act(
        "Charmaine Neville",
        NEWORLEANS,
        SAT,
        t(15, 50),
        t(17, 0),
        genre=Genre.JAZZ_CONTEMPORARY,
        about=(
            "Daughter of Charles Neville of the Neville Brothers, Charmaine\n"
            "Neville is a powerhouse vocalist who has been a fixture of New\n"
            "Orleans nightlife since the mid-1980s, holding down a legendary\n"
            "residency at Snug Harbor with keyboardist Amasa Miller. Her jazz\n"
            "and funk-inflected sets draw on collaborations with Dr. John,\n"
            "Harry Connick Jr., and Bobby McFerrin, and she is a passionate\n"
            "advocate for the preservation of the city's musical culture."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.charmainenevilleband.com"],
    ),
    Act(
        "James Andrews",
        NEWORLEANS,
        SAT,
        t(17, 20),
        t(18, 45),
        genre=Genre.BRASS_BAND,
        about=(
            "Known as the 'Satchmo of the Ghetto,' James Andrews is a Treme-raised\n"
            "trumpeter and vocalist whose musical bloodline runs deep \u2014 he is the\n"
            "older brother of Trombone Shorty and grandson of Jesse Hill. After\n"
            "cutting his teeth with the Treme Brass Band and New Birth Brass Band,\n"
            "he formed the Crescent City Allstars. His 1998 album, produced by\n"
            "Allen Toussaint with Dr. John on every track, is a local classic."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.crescentcityallstars.com"],
    ),
    # ── Tropical Isle Hand Grenade Stage ──────────────────────────────
    Act(
        "Christian Serpas & Ghost Town",
        TROPICAL,
        SAT,
        t(11, 10),
        t(12, 10),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "For twenty-five years Christian Serpas & Ghost Town have been one of\n"
            "the Gulf South's best live acts, blending honky-tonk lyrics with\n"
            "scorching rock-and-roll guitars in what critics call 'twangified\n"
            "rock 'n' roll.' Inducted into the Louisiana Music Hall of Fame in\n"
            "2024, they have shared stages with Kenny Chesney, Merle Haggard,\n"
            "Dwight Yoakam, and nearly a hundred other touring acts."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://csghosttown.com"],
    ),
    Act(
        "Ovi-G presents 'Xtra Cash!'",
        TROPICAL,
        SAT,
        t(12, 30),
        t(13, 30),
        genre=Genre.RNB_SOUL,
        about=(
            "Ovi-G's Xtra Cash is a New Orleans-based ensemble bringing\n"
            "high-energy R&B, hip-hop, and bounce vibes to the festival\n"
            "stage. A rising act on the local scene, the band has been\n"
            "building a following through packed club dates and social\n"
            "media buzz, delivering crowd-pleasing sets that keep the\n"
            "dance floor moving."
        ),
        about_source=AboutSource.GENERATED,
        websites=["https://www.instagram.com/xtra__cash/"],
    ),
    Act(
        "Ronnie Lamarque Orchestra feat. Hot Rod Lincoln",
        TROPICAL,
        SAT,
        t(14, 0),
        t(15, 15),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Auto mogul, Louisiana Music Hall of Fame inductee, and old-school\n"
            "crooner Ronnie Lamarque fronts a twenty-one-piece orchestra that\n"
            "delivers big-band tunes in the Frank Sinatra and Bobby Darin mold.\n"
            "Hot Rod Lincoln is a Sha Na Na-style oldies act of lawyers and\n"
            "businessmen, and together the combined bill makes for a joyful,\n"
            "retro variety show that is pure New Orleans spectacle."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.lamarque.com"],
    ),
    Act(
        "Victor Campbell & Timba Swamp",
        TROPICAL,
        SAT,
        t(15, 35),
        t(16, 35),
        genre=Genre.LATIN,
        about=(
            "Cuban-born pianist Victor Campbell trained at Cuba's National School\n"
            "of the Arts and relocated to New Orleans in 2019, quickly integrating\n"
            "local blues and jazz flavors into his Afro-Cuban repertoire. Timba\n"
            "Swamp is his band project focused on timba \u2014 a high-octane Cuban\n"
            "dance genre \u2014 blending it with New Orleans rhythms. Their 2026\n"
            "French Quarter Fest appearance is a debut not to miss."
        ),
        about_source=AboutSource.RESEARCHED,
    ),
    Act(
        "Flagboy Giz & the Wild Tchoupitoulas",
        TROPICAL,
        SAT,
        t(16, 55),
        t(17, 55),
        genre=Genre.INDIAN_MARDI_GRAS,
        about=(
            "Flagboy Giz (Aaron Hartley) is a fifth-generation New Orleanian and\n"
            "member of the Wild Tchoupitoulas, one of the city's most historic\n"
            "Black masking Indian tribes. His breakout single 'We Outside' racked\n"
            "up over a million YouTube views and was licensed by the NFL for\n"
            "Super Bowl LIX. He also contributed costume work to Marvel's Black\n"
            "Panther sequel. Expect chants, beadwork, and serious energy."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://flagboygiz.com"],
    ),
    Act(
        "Higher Heights Reggae Band",
        TROPICAL,
        SAT,
        t(18, 15),
        t(19, 45),
        genre=Genre.REGGAE,
        about=(
            "Higher Heights has been anchoring the New Orleans reggae scene since\n"
            "2000. Founded by keyboardist Cheryl McKay, the five-piece ensemble\n"
            "won Offbeat's Best New Emerging Artist in 2002 and spent a decade\n"
            "touring with the Bob Marley Festival, sharing stages with Steel\n"
            "Pulse, Burning Spear, and Yellowman. They are fixtures at Jazz Fest,\n"
            "FQF, and Cafe Negril on Frenchmen Street."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.facebook.com/p/Higher-Heights-Reggae-100063571297868/"],
    ),
    # ── Jack Daniel's Stage ───────────────────────────────────────────
    Act(
        "Lily Unless and The If Onlys",
        JACKDANIELS,
        SAT,
        t(11, 10),
        t(12, 30),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "Lily Unless & The If Onlys are a four-piece New Orleans band\n"
            "serving up original country, rockabilly, and early rock 'n' roll\n"
            "with honky-tonk grit and blues undertones. Formed in the city,\n"
            "they have been building a devoted following through spirited live\n"
            "shows at local venues and touring across the South."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://lilyunlessandtheifonlys.bandcamp.com"],
    ),
    Act(
        "Paul Sanchez",
        JACKDANIELS,
        SAT,
        t(12, 50),
        t(13, 50),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "A founding member of Cowboy Mouth and one of New Orleans' most\n"
            "prolific songwriters, Paul Sanchez has penned material covered by\n"
            "Irma Thomas, Darius Rucker, and Hootie and the Blowfish. He\n"
            "appeared as himself on HBO's Treme. After Katrina, his tribute\n"
            "song 'Home' became an anthem featured in the documentary New\n"
            "Orleans Music in Exile."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://paulsanchez.com"],
    ),
    Act(
        "Water Seed",
        JACKDANIELS,
        SAT,
        t(14, 10),
        t(15, 10),
        genre=Genre.FUNK,
        about=(
            "Water Seed is a New Orleans-based contemporary funk and soul band\n"
            "that coined the term 'Future Funk' to describe their fusion of\n"
            "funk, rock, hip-hop, and jazz. Founded by drummer Lou Hill, the\n"
            "group cultivated in Atlanta post-Katrina before returning home\n"
            "in 2014 and headlining a sold-out night at Harlem's Apollo\n"
            "Theater. Their immersive 'Journey to Funkstar' concerts blend\n"
            "music with visual storytelling."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://waterseed.bandcamp.com"],
    ),
    Act(
        "Iceman Special",
        JACKDANIELS,
        SAT,
        t(15, 30),
        t(16, 40),
        genre=Genre.ROCK,
        about=(
            "The Iceman Special is a four-piece Louisiana swamp-funk outfit\n"
            "that transplanted from the bayous to New Orleans proper. Brothers\n"
            "Will and Charlie Murry, guitarist Steve Staples, and drummer\n"
            "Hunter Romero blend dirty funk, disco, psych-rock, and reggae\n"
            "into danceable jams. They have headlined Tipitina's, graced\n"
            "the cover of Offbeat, and launched their own music festival."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.theicemanspecial.com"],
    ),
    Act(
        "The Original Pinettes Brass Band",
        JACKDANIELS,
        SAT,
        t(17, 0),
        t(18, 20),
        genre=Genre.BRASS_BAND,
        about=(
            "New Orleans' only all-female brass band, The Original Pinettes were\n"
            "founded in 1991 at St. Mary's Academy. They won the 2013 Red Bull\n"
            "'Street Kings' brass band blowout, prompting the name change to\n"
            "'Street Queens,' and played the Met Gala afterparty for Katy Perry\n"
            "in 2017. Their Friday-night residency at Bullet's Sports Bar in\n"
            "the Seventh Ward is a local institution."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.originalpinettes.com"],
    ),
    Act(
        "Big Freedia",
        JACKDANIELS,
        SAT,
        t(18, 50),
        t(20, 0),
        genre=Genre.ELECTRONIC_DJ,
        about=(
            "The undisputed Queen of Bounce, Big Freedia has propelled New\n"
            "Orleans' bounce music from the projects to the global stage.\n"
            "Her voice anchors Beyonce's 'Formation' and the Grammy-winning\n"
            "'Break My Soul,' and her Fuse reality show introduced the culture\n"
            "to millions. Freedia's live sets are communal dance parties driven\n"
            "by call-and-response chants and relentless energy \u2014 expect the\n"
            "whole block to be twerking."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.instagram.com/bigfreedia/"],
    ),
    # ── Willow Dispensary Stage ───────────────────────────────────────
    Act(
        "Bruce Daigrepont Cajun Band",
        WILLOW,
        SAT,
        t(11, 10),
        t(12, 20),
        genre=Genre.CAJUN,
        about=(
            "Accordionist Bruce Daigrepont is a fixture of New Orleans Cajun music.\n"
            "Born in the city to Cajun transplants from rural Louisiana, he was so\n"
            "inspired by the Festival Acadiens in 1978 that he learned the French\n"
            "accordion and formed his own band. His Sunday fais do-do at Tipitina's\n"
            "ran for thirty years, making him the venue's all-time performance\n"
            "leader with over 1,400 shows on that stage alone."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["http://www.brucedaigrepont.org"],
    ),
    Act(
        "Magnolia Sisters",
        WILLOW,
        SAT,
        t(12, 40),
        t(13, 50),
        genre=Genre.CAJUN,
        about=(
            "The Magnolia Sisters may be Cajun music's only all-woman band,\n"
            "featuring Ann Savoy, Jane Vidrine, Anya Burgess, and Lisa Trahan.\n"
            "Based in Lafayette, they deliver energetic dance tunes alongside\n"
            "wistful ballads drawn from deep in the roots of Acadiana. Their\n"
            "beautiful harmonies and rediscovery of little-known traditional\n"
            "repertoire have earned two Grammy-nominated albums and extensive\n"
            "touring in Europe and the US."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://magnoliasisters.com"],
    ),
    Act(
        "Donna Angelle & the Zydeco Posse",
        WILLOW,
        SAT,
        t(14, 10),
        t(15, 10),
        genre=Genre.ZYDECO,
        about=(
            "Donna Angelle was born in Cypress Island, Louisiana, and broke\n"
            "barriers as a female bandleader in the male-dominated zydeco world.\n"
            "A multi-instrumentalist who cut her chops on bass with Barbara Lynn\n"
            "and Archie Bell, she now fronts the Zydeco Posse on accordion,\n"
            "calling down dance-groove stylings that blend old-school hip-hop,\n"
            "soul, and zydeco. She has toured as far as Africa and Europe."
        ),
        about_source=AboutSource.RESEARCHED,
    ),
    Act(
        "Corey Ledet Zydeco & Black Magic",
        WILLOW,
        SAT,
        t(15, 30),
        t(16, 40),
        genre=Genre.ZYDECO,
        about=(
            "Known as 'The Accordion Dragon,' Corey Ledet has mastered the\n"
            "piano-accordion style of Clifton Chenier and earned two Grammy\n"
            "nominations across sixteen albums. His all-black custom Italian\n"
            "accordion \u2014 'Black Magic' \u2014 lends its name to his band, which\n"
            "combusts zydeco, blues, jazz, and guitar-shredding rock into\n"
            "dance-floor fuel. His latest, Live In Alaska, captures that\n"
            "energy in full."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://coreyledet.com"],
    ),
    Act(
        "Dwayne Dopsie and the Zydeco Hellraisers",
        WILLOW,
        SAT,
        t(17, 0),
        t(18, 10),
        genre=Genre.ZYDECO,
        about=(
            "Son of zydeco pioneer Rockin' Dopsie Sr., Dwayne Dopsie has been\n"
            "playing accordion since age seven and was named 'America's Hottest\n"
            "Accordionist' at nineteen. The Zydeco Hellraisers earned a 2018\n"
            "Grammy nomination for Best Regional Roots Album and multiple\n"
            "Offbeat awards. Dwayne's high-energy style blends traditional\n"
            "zydeco with funk, R&B, rock, and reggae, defying every stereotype."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://dwaynedopsie.com"],
    ),
    Act(
        "Sweet Crude",
        WILLOW,
        SAT,
        t(18, 30),
        t(20, 0),
        genre=Genre.ROCK,
        about=(
            "Sweet Crude is a six-piece New Orleans band that sets English and\n"
            "Louisiana French to decidedly non-Cajun music \u2014 think five-part\n"
            "harmonies, tribal rhythms, and pop hooks. With surnames like\n"
            "Marceaux, Arceneaux, and Chachere, the members reconnect with\n"
            "their heritage through indie pop and rock. They signed with\n"
            "Verve Forecast and released their major-label debut Officiel/\n"
            "Artificiel in 2020."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.sweetcrudeband.com"],
    ),
    # ── Loyola Esplanade in the Shade Stage ───────────────────────────
    Act(
        "Loyola University Commercial Ensemble",
        LOYOLA,
        SAT,
        t(11, 0),
        t(12, 15),
        genre=Genre.JAZZ_CONTEMPORARY,
        about=(
            "Loyola University's College of Music and Media has one of the oldest\n"
            "jazz programs in New Orleans, with alumni including Wynton Marsalis\n"
            "and Terence Blanchard. The Commercial Ensemble showcases advanced\n"
            "students performing contemporary jazz, funk, and popular repertoire\n"
            "under the guidance of top-shelf faculty who gig across the city."
        ),
        about_source=AboutSource.GENERATED,
    ),
    Act(
        "Joy Clark",
        LOYOLA,
        SAT,
        t(12, 35),
        t(13, 45),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "Louisiana-born singer-songwriter Joy Clark grew up in a tight-knit\n"
            "New Orleans gospel family and has since toured with Grammy winners\n"
            "Allison Russell and Cyril Neville. Her debut album Tell It to the\n"
            "Wind, released on Righteous Babe Records, explores self-discovery\n"
            "as a Black, queer young woman in the South. Her songcraft pairs\n"
            "sophisticated progressions with themes of freedom and love."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://joyclarkmusic.com"],
    ),
    Act(
        "Tay/Heavensworld/Ja Fierce & Azure Skye et al.",
        LOYOLA,
        SAT,
        t(14, 10),
        t(15, 30),
        genre=Genre.RNB_SOUL,
        about=(
            "This multi-artist showcase highlights a collective of emerging New\n"
            "Orleans R&B, hip-hop, and soul performers sharing the stage for a\n"
            "collaborative set. The billing brings together Tay, Heavensworld,\n"
            "Ja Fierce, Azure Skye, and friends, representing the next wave of\n"
            "the city's vibrant young music scene."
        ),
        about_source=AboutSource.GENERATED,
    ),
    Act(
        "Mia Borders",
        LOYOLA,
        SAT,
        t(15, 50),
        t(17, 10),
        genre=Genre.RNB_SOUL,
        about=(
            "Born and raised in New Orleans, Mia Borders is a singer-songwriter\n"
            "who mixes soul, funk, R&B, and electronic textures across a deep\n"
            "catalog of self-released albums on her own Blaxican Records. Her\n"
            "latest, Firewalker, channels resilient New Orleans funk. Off stage\n"
            "she runs Third Coast Entertainment, a booking agency elevating\n"
            "women, LGBTQ+, and BIPOC artists, and founded The Borders\n"
            "Foundation to support marginalized musicians."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.miaborders.com"],
    ),
    Act(
        "John 'Papa' Gros",
        LOYOLA,
        SAT,
        t(17, 30),
        t(19, 0),
        genre=Genre.FUNK,
        about=(
            "Keyboardist, singer, and songwriter John 'Papa' Gros is a bedrock\n"
            "New Orleans artist who draws on funk, R&B, Americana, and Mardi\n"
            "Gras repertoire. He founded Papa Grows Funk, which held an epic\n"
            "twelve-year Monday night residency at the Maple Leaf Bar. Now a\n"
            "solo touring act, he has served as go-to keys man for Little Feat,\n"
            "the Neville Brothers, the Funky Meters, and Anders Osborne."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://johnpapagros.com"],
    ),
    # ── Louisiana Fish Fry Stage ──────────────────────────────────────
    Act(
        "Red Wolf Brass Band",
        FISHFRY,
        SAT,
        t(11, 10),
        t(12, 30),
        genre=Genre.BRASS_BAND,
        about=(
            "Founded by trumpeter Desmond 'Black Moses' Venable, the Red Wolf\n"
            "Brass Band puts a new swing on traditional New Orleans music. Their\n"
            "debut CD '7th Period' features timeless classics and originals with\n"
            "guest spots from Shamarr Allen and members of the Soul Rebels.\n"
            "They bring jazz back to its roots as dance music, blending old and\n"
            "new schools with infectious charisma."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.redwolfbrassband.com"],
    ),
    Act(
        "DJ Hollaback",
        FISHFRY,
        SAT,
        t(12, 35),
        t(13, 5),
        genre=Genre.ELECTRONIC_DJ,
        about=(
            "DJ Hollaback is a New Orleans DJ who spins at the Fish Fry Stage\n"
            "between brass band sets, keeping the second-line energy going with\n"
            "a mix of bounce, hip-hop, and R&B party anthems that keep the\n"
            "crowd moving between live acts."
        ),
        about_source=AboutSource.GENERATED,
    ),
    Act(
        "Storyville Stompers Brass Band",
        FISHFRY,
        SAT,
        t(13, 10),
        t(14, 30),
        genre=Genre.BRASS_BAND,
        about=(
            "Established in 1981 and led by sousaphonist Woody Penouilh, the\n"
            "Storyville Stompers are one of the nation's preeminent traditional\n"
            "brass bands. With over 6,000 performances across the US, Europe,\n"
            "South America, and Asia, they stay faithful to the roots while\n"
            "most modern brass bands lean into funk and R&B. Their sound is\n"
            "pure, joyful New Orleans tradition."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["http://www.storyvillestompers.com"],
    ),
    Act(
        "DJ Spin",
        FISHFRY,
        SAT,
        t(14, 35),
        t(15, 15),
        genre=Genre.ELECTRONIC_DJ,
        about=(
            "DJ Spin takes the Fish Fry Stage between brass band performances,\n"
            "delivering an eclectic mix of New Orleans bounce, hip-hop, and\n"
            "crowd-pleasing party tracks that bridge the gap between live sets\n"
            "and keep the dance floor packed."
        ),
        about_source=AboutSource.GENERATED,
    ),
    Act(
        "Original Hurricane Brass Band",
        FISHFRY,
        SAT,
        t(15, 20),
        t(16, 40),
        genre=Genre.BRASS_BAND,
        about=(
            "Originally founded in 1974 by trumpet legend Leroy Jones around\n"
            "the core of the Fairview Baptist Church Brass Band, the Hurricane\n"
            "Brass Band was an undeniable force on the local second-line scene\n"
            "and helped pioneer what became contemporary New Orleans brass\n"
            "music. Members went on to form the Dirty Dozen Brass Band, and\n"
            "the original ensemble's legacy lives on in every modern brass\n"
            "band that followed."
        ),
        about_source=AboutSource.RESEARCHED,
    ),
    Act(
        "DJ RQ Away",
        FISHFRY,
        SAT,
        t(16, 45),
        t(17, 30),
        genre=Genre.ELECTRONIC_DJ,
        about=(
            "New Orleans-bred DJ RQ Away is head of the #Awayteam community\n"
            "and a genre-bending selector whose sets span house, hip-hop,\n"
            "funk, disco, bounce, and beyond. He has spun alongside Robert\n"
            "Glasper, Erykah Badu, and Bilal, and his ability to create a\n"
            "distinct vibe has captured ears from Frenchmen Street to the\n"
            "pubs of London."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://djrqaway.com"],
    ),
    Act(
        "Big 6 Brass Band",
        FISHFRY,
        SAT,
        t(17, 35),
        t(18, 55),
        genre=Genre.BRASS_BAND,
        about=(
            "Founded in 2017 by members and alumni of Rebirth, Hot 8, and\n"
            "Stooges brass bands, the Big 6 quickly became the most popular\n"
            "band on the second-line streets of their native Sixth Ward.\n"
            "Their debut album was hailed by Offbeat as 'the sound of New\n"
            "Orleans streets today,' blending smooth R&B vocals with the\n"
            "rough-and-ready brass band tradition."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://bigsixbrassband.com"],
    ),
    Act(
        "DJ Poppa",
        FISHFRY,
        SAT,
        t(19, 0),
        t(20, 0),
        genre=Genre.ELECTRONIC_DJ,
        about=(
            "DJ Poppa is a crowd favorite known for his legendary bounce\n"
            "mixes, blending old-school classics with cutting-edge fresh\n"
            "flavors. A regular at New Orleans clubs and an in-demand event\n"
            "entertainer, he closes out the Fish Fry Stage with high-energy\n"
            "sets that send the Saturday crowd home dancing."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.instagram.com/teamdjpoppa/"],
    ),
    # ── Entergy Songwriter Stage ──────────────────────────────────────
    Act(
        "John Rankin",
        ENTERGY,
        SAT,
        t(11, 0),
        t(11, 55),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "John Rankin has been a featured performer at Jazz Fest since 1981\n"
            "and is a versatile master of solo acoustic guitar who blends folk,\n"
            "blues, jazz, classical, and R&B with a true New Orleans feel. He\n"
            "taught guitar and songwriting at Loyola for over thirty years and\n"
            "received Offbeat's Lifetime Achievement Award in Music Education.\n"
            "His powerful harmonica playing adds real impact to his songs."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://johnrankin.net"],
    ),
    Act(
        "Beth Patterson",
        ENTERGY,
        SAT,
        t(12, 15),
        t(13, 10),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "A Lafayette native and New Orleans transplant, Beth Patterson\n"
            "combines Irish, Celtic, and folk traditions with Cajun, world-beat,\n"
            "and prog-rock influences on the Irish bouzouki \u2014 a teardrop-shaped\n"
            "eight-string instrument she plays with fiery skill. She has toured\n"
            "twenty countries, released nine solo albums, and recently appeared\n"
            "in the pub band in Spinal Tap II."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://bethpattersonmusic.com"],
    ),
    Act(
        "Kyle Alexander",
        ENTERGY,
        SAT,
        t(13, 30),
        t(14, 25),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "Kyle Alexander is a singer-songwriter and multi-instrumentalist\n"
            "whose self-produced work spans pop, R&B, funk, alternative, and\n"
            "psychedelic sounds. Making his French Quarter Fest debut in 2026\n"
            "on the Entergy Songwriter Stage, he brings an introspective\n"
            "songwriting style shaped by travels and a DIY ethos."
        ),
        about_source=AboutSource.GENERATED,
    ),
    Act(
        "Daphne Parker Powell",
        ENTERGY,
        SAT,
        t(14, 45),
        t(15, 45),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "Originally from New London, Connecticut, Daphne Parker Powell moved\n"
            "to New Orleans and developed a swampy, dance-ready 'torch folk'\n"
            "sound blending jazz, pop, and R&B. Her forthcoming album The Death\n"
            "of Cool was produced by Jimbo Mathus and features collaborations\n"
            "with Preservation Hall and Squirrel Nut Zippers musicians. Bold\n"
            "horn charts, gritty Southern guitar, and poetic storytelling\n"
            "define her sets."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.daphneparkerpowell.com"],
    ),
    Act(
        "AdoSoul and the Tribe",
        ENTERGY,
        SAT,
        t(16, 5),
        t(17, 0),
        genre=Genre.FUNK,
        about=(
            "Self-described as 'The Soul Heir to Funk,' AdoSoul and the Tribe\n"
            "deliver a potent blend of funk, blues, and New Orleans soul. The\n"
            "band is a story of second chances and the sacred grind of becoming,\n"
            "featuring fiery horn arrangements from Alijah Jett and thunderous\n"
            "guitar work from Gregg Molinario. They have performed at the\n"
            "New Orleans Jazz Museum and venues across the city."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://adosoulmusic.com"],
    ),
    # ── Pan-American Life Insurance Group Stage ───────────────────────
    Act(
        "Legendary Barbara Shorts and Blue Jazz",
        PANAMLIFE,
        SAT,
        t(11, 0),
        t(12, 10),
        genre=Genre.GOSPEL,
        about=(
            "At seventy-five, Barbara Shorts possesses one of the most powerful\n"
            "voices on any New Orleans stage. Raised in the gospel church, she\n"
            "earned fame as Big Bertha Williams in the hit musical One Mo' Time\n"
            "and co-founded the Gospel Soul Children. After a thirteen-year\n"
            "hiatus she returned to performing and recording, bringing a\n"
            "lifetime of gospel, jazz, and blues conviction to every note."
        ),
        about_source=AboutSource.RESEARCHED,
    ),
    Act(
        "Lynn Drury",
        PANAMLIFE,
        SAT,
        t(12, 30),
        t(13, 30),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "Originally from the Mississippi Delta, Lynn Drury has spent over\n"
            "two decades honing what she calls 'NOLAmericana' \u2014 Americana\n"
            "songwriting steeped in New Orleans grooves. She won Offbeat's\n"
            "Best Country Singer/Songwriter award in 2003 and has released\n"
            "ten albums of originals, including 2024's High Tide. Her sultry,\n"
            "sweet songs can turn funky at the drop of a hat."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://lynndrury.com"],
    ),
    Act(
        "Vivaz",
        PANAMLIFE,
        SAT,
        t(13, 50),
        t(14, 50),
        genre=Genre.LATIN,
        about=(
            "Led by Bolivian-born guitarist and vocalist Javier Gutierrez,\n"
            "Vivaz incorporates jazz, Brazilian, flamenco, and tropical\n"
            "flavors into an energetic Latin sound. Gutierrez came to New\n"
            "Orleans from La Paz in the early 1980s and built the band into\n"
            "a mainstay of the city's Latin music and salsa-dancing scene,\n"
            "performing at festivals and dance events for decades."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.vivazmusic.com"],
    ),
    Act(
        "Ever More Nest",
        PANAMLIFE,
        SAT,
        t(15, 10),
        t(16, 10),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "Ever More Nest is a New Orleans Americana project rooted in\n"
            "Southern musical traditions and infused with confessional '90s\n"
            "angst. Led by vocalist Kelcy Mae Wilburn and backed by a family\n"
            "of musicians on banjo, mandolin, fiddle, and guitars, the band\n"
            "delivers lush, church-pew harmonies over expansive arrangements.\n"
            "Their debut was nominated for Best Alt-Country Album at the\n"
            "Independent Music Awards."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://evermorenest.com"],
    ),
    Act(
        "Troy Sawyer and the Elementz",
        PANAMLIFE,
        SAT,
        t(16, 30),
        t(17, 50),
        genre=Genre.MIXED_ECLECTIC,
        about=(
            "Grammy Recording Academy member Troy Sawyer is an award-winning\n"
            "trumpeter, composer, and educator from New Orleans whose great-\n"
            "grandfather co-wrote songs with Buddy Bolden. The Elementz fuse\n"
            "funk, rock, soul, jazz, and Latin into a musical gumbo that\n"
            "earned Troy the OffBeat Millennial Award and Emerging Artist\n"
            "of the Year from the New Orleans Tourism and Cultural Fund.\n"
            "He also founded Girls Play Trumpets Too, a nonprofit empowering\n"
            "young female musicians."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.troysawyermusic.com"],
    ),
    Act(
        "Ferm\u00edn Ceballos + Merengue4FOUR",
        PANAMLIFE,
        SAT,
        t(18, 10),
        t(19, 30),
        genre=Genre.LATIN,
        about=(
            "Dominican-born guitarist, accordionist, and singer Ferm\u00edn Ceballos\n"
            "moved to New Orleans in 2012 and quickly wove local sounds into\n"
            "his Afro-Caribbean repertoire. Merengue4FOUR is his project focused\n"
            "on merengue t\u00edpico and bachata, and his album Bochinche includes\n"
            "'Zydeco Star,' a collaboration with Rockin' Dopsie Jr. that\n"
            "captures the joyful collision of Dominican and Louisiana rhythms."
        ),
        about_source=AboutSource.RESEARCHED,
    ),
    # ── Jazz Playhouse at the Royal Sonesta ───────────────────────────
    Act(
        "Audrey Lecrone",
        JAZZPLAYHOUSE,
        SAT,
        t(11, 0),
        t(13, 30),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "A third-generation musician from Kansas who found her voice after\n"
            "moving to New Orleans, Audrey Lecrone moonlights as an acclaimed\n"
            "dialect coach \u2014 she guided Daniel Kaluuya's Oscar-winning performance\n"
            "in Judas and the Black Messiah. Her show blends silky vocals,\n"
            "masterful improvisation, and playful banter, and with her band\n"
            "the CrawZaddies she has become one of the city's hottest new\n"
            "jazz acts."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.audreylecronemusic.com"],
    ),
    Act(
        "The Wolfe Johns Blues Band",
        JAZZPLAYHOUSE,
        SAT,
        t(14, 0),
        t(16, 30),
        genre=Genre.BLUES,
        about=(
            "The Wolfe Johns Blues Band is a New Orleans three-piece that draws\n"
            "on influences reaching back to the 1930s \u2014 John Lee Hooker,\n"
            "Lightnin' Slim, Muddy Waters, and Robert Johnson \u2014 while writing\n"
            "high-energy originals of their own. During the pandemic Wolfe Johns\n"
            "performed daily on Royal Street, becoming a French Quarter fixture.\n"
            "They have shared stages with Little Freddie King, Jon Cleary, and\n"
            "Charlie Musselwhite."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://wjblues.com"],
    ),
    Act(
        "Richard 'Piano' Scott & The Twisty River Band",
        JAZZPLAYHOUSE,
        SAT,
        t(17, 0),
        t(19, 30),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Richard 'Piano' Scott is a multi-instrumentalist and former longtime\n"
            "member of the Dukes of Dixieland who now leads the Twisty River Band.\n"
            "The group specializes in the greatest songs to come out of New\n"
            "Orleans and the early jazz era, performing them with irresistible\n"
            "warmth and swing. Their albums Port of New Orleans and Hey Day\n"
            "Drinkers feature originals alongside deep-cut standards."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.richardpianoscott.com"],
    ),
    # ── French Market Traditional Jazz Stage ──────────────────────────
    Act(
        "Secret Six Jazz Band",
        FRENCHMARKET,
        SAT,
        t(11, 30),
        t(13, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "The Secret Six took shape during the pandemic when members of the\n"
            "Smoking Time Jazz Band took their instruments to parks and porches\n"
            "to keep the music alive. They have since become one of New Orleans'\n"
            "most exciting traditional jazz ensembles, handling stomps, blues,\n"
            "rags, and hot jazz with deep-cut repertoire from King Oliver,\n"
            "Louis Armstrong's Hot Five, and the New Orleans revival era."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.secretsixjazzband.com"],
    ),
    Act(
        "Special Dance Performance by the NOLA Chorus Girls",
        FRENCHMARKET,
        SAT,
        t(13, 0),
        t(13, 5),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "The NOLA Chorus Girls are a New Orleans dance troupe inspired by\n"
            "female dancers of the jazz age. Formed in 2011, this ensemble of\n"
            "fabulous flappers celebrates jazz-era movement and style, welcoming\n"
            "women of all ages and ability levels to perform."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.facebook.com/thenolachorusgirls"],
    ),
    Act(
        "New Orleans Cottonmouth Kings",
        FRENCHMARKET,
        SAT,
        t(13, 30),
        t(15, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "The Cottonmouth Kings bring a touch of Paris to Frenchmen Street\n"
            "and beyond with hot jazz classics ranging from traditional New\n"
            "Orleans jazz to big-band swing. Featuring clarinetist Bruce\n"
            "Brackman, trumpeter Charlie Fardella, and violinist Matt Rhody\n"
            "among others, they focus on obscure gems from the trad jazz\n"
            "canon, all performed with impeccable energy and style."
        ),
        about_source=AboutSource.RESEARCHED,
    ),
    Act(
        "Alicia Renee aka Blue Eyes Sextet",
        FRENCHMARKET,
        SAT,
        t(15, 30),
        t(17, 0),
        genre=Genre.JAZZ_CONTEMPORARY,
        about=(
            "Born in Flint, Michigan and nicknamed for her striking natural\n"
            "blue eyes, Alicia Renee spent a decade performing in Switzerland\n"
            "before bringing her voice to New Orleans. Her versatility spans\n"
            "opera, jazz, gospel, blues, and R&B, and she has performed with\n"
            "Eric Clapton, Roy Hargrove, the Preservation Hall Jazz Band, and\n"
            "Jon Batiste. She is a regular at Preservation Hall and Snug Harbor."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://aliciareneeakablueeyes.com"],
    ),
    Act(
        "The Jump Hounds",
        FRENCHMARKET,
        SAT,
        t(17, 30),
        t(19, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Founded in 2018, The Jump Hounds are a New Orleans sextet\n"
            "specializing in 'jump' \u2014 the jazz-based R&B that bridged swing\n"
            "and rock 'n' roll. Led by Marty Peters on sax and Adam Arredondo\n"
            "on trumpet, they transcribe material from the original masters\n"
            "while writing new tunes within the idiom, delivering energetic\n"
            "up-tempo numbers, slow blues, and cozy mid-tempo swingers."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.thejumphounds.com"],
    ),
    # ── French Market Dutch Alley Stage ───────────────────────────────
    Act(
        "Kid Simmons Jazz Band",
        DUTCHALLEY,
        SAT,
        t(11, 15),
        t(12, 30),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Born in London in 1943, John 'Kid' Simmons first visited New\n"
            "Orleans in 1964 and made it home by 1970. He joined the Young\n"
            "Tuxedo Brass Band in 1973 and has led bands at Preservation Hall\n"
            "and Maison Bourbon. For over a decade his small ensemble has been\n"
            "a fixture at French Quarter Festival and he leads the International\n"
            "All Stars at Jazz Fest."
        ),
        about_source=AboutSource.RESEARCHED,
    ),
    Act(
        "Stephen Walker N'Em Swinging in New Orleans",
        DUTCHALLEY,
        SAT,
        t(12, 45),
        t(14, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Trombonist Stephen Walker began playing at age five and studied\n"
            "at the New Orleans Center for Creative Arts before touring\n"
            "internationally at sixteen with Grammy-winner Irvin Mayfield.\n"
            "Mentored by Delfeayo Marsalis and currently touring with the\n"
            "Dirty Dozen Brass Band, Walker's ensemble blends gospel roots,\n"
            "traditional jazz, funk, Latin, and contemporary sounds into\n"
            "one swinging package."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.stephenwalkermusic.com"],
    ),
    Act(
        "Kevin Ray Clark and Bourbon Street All Stars",
        DUTCHALLEY,
        SAT,
        t(14, 15),
        t(15, 30),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Three-time Grammy nominee and Grammy winner Kevin Ray Clark is\n"
            "the music director at Fritzel's, Bourbon Street's oldest jazz\n"
            "club. After stints with Ringling Bros. and Walt Disney World, he\n"
            "moved to New Orleans in 1992 and has performed with Pete Fountain,\n"
            "the Dukes of Dixieland, and the New Orleans Nightcrawlers. His\n"
            "Bourbon Street All Stars keep traditional jazz alive nightly."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://kevinrayclark.com"],
    ),
    Act(
        "New Orleans Ragtime Orchestra ft. Lars Edegran",
        DUTCHALLEY,
        SAT,
        t(15, 45),
        t(17, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Swedish-born pianist Lars Edegran moved to New Orleans in 1966 and\n"
            "founded the New Orleans Ragtime Orchestra to perform classic rags,\n"
            "cakewalks, and pieces from the 1890s\u20131920s era. The orchestra's\n"
            "work on Louis Malle's Pretty Baby earned an Academy Award\n"
            "nomination. Nine albums and nearly six decades later, they remain\n"
            "the gold standard for ragtime performance in the city."
        ),
        about_source=AboutSource.RESEARCHED,
    ),
    # ── House of Blues Voodoo Garden Stage ─────────────────────────────
    Act(
        "Tiago Guy & Renee Gros",
        HOUSEOFBLUES,
        SAT,
        t(11, 15),
        t(12, 30),
        genre=Genre.RNB_SOUL,
        about=(
            "Husband-and-wife duo Tiago Guy and Renee Gros are a powerhouse\n"
            "soul and roots-music collaboration. Tiago, a Brazilian guitarist\n"
            "steeped in American R&B and gospel, arrived in New Orleans in\n"
            "2021. Renee, a New Orleans native and self-proclaimed 'Dive Bar\n"
            "Diva,' blends folk storytelling with Southern rock and soul.\n"
            "Together they made their Jazz Fest debut in 2024."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.reneegros.com", "https://tiagoguy.com"],
    ),
    Act(
        "Pocket Chocolate",
        HOUSEOFBLUES,
        SAT,
        t(12, 45),
        t(14, 45),
        genre=Genre.FUNK,
        about=(
            "Pocket Chocolate is a seven-piece funk, blues, and soul collective\n"
            "made up entirely of born-and-raised New Orleans musicians. Formed\n"
            "in 2019, they blend original songwriting with samples from across\n"
            "genres, delivering a modern take on the styles that founded the\n"
            "city's musical culture. Their debut EP Live From New Orleans\n"
            "captures the raw energy of their Gulf Coast shows."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.pocketchocolatemusic.com"],
    ),
    Act(
        "Jamey St. Pierre",
        HOUSEOFBLUES,
        SAT,
        t(15, 0),
        t(17, 0),
        genre=Genre.BLUES,
        about=(
            "Jamey St. Pierre is a New Orleans singer-songwriter whose soulful\n"
            "voice sprouted from childhood church hymns and his mother's front-\n"
            "porch guitar. Whether solo or fronting his dance-inspiring quintet\n"
            "the Honeycreepers, he delivers original songs drenched in New\n"
            "Orleans blues alongside interpretations of Bill Withers, Nina\n"
            "Simone, and Allen Toussaint. He calls his style 'New Orleans\n"
            "Authentic Soul.'"
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://jameystpierremusic.com"],
    ),
    Act(
        "Eric Johanson",
        HOUSEOFBLUES,
        SAT,
        t(17, 15),
        t(19, 15),
        genre=Genre.BLUES,
        about=(
            "Louisiana-born guitarist and singer Eric Johanson was discovered\n"
            "by Tab Benoit and signed to Whiskey Bayou Records. Named one of\n"
            "Guitar Player's 25 Best New Blues Guitarists and featured on Total\n"
            "Guitar's Greatest Blues Guitarists list, his 2023 album The Deep\n"
            "and the Dirty debuted at number one on the Billboard blues chart.\n"
            "He has toured with Cyril Neville, Anders Osborne, and the Neville\n"
            "Brothers."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.ericjohanson.com"],
    ),
    Act(
        "Sansone & John Fohl",
        HOUSEOFBLUES,
        SAT,
        t(19, 30),
        t(21, 30),
        genre=Genre.BLUES,
        about=(
            "Johnny Sansone is a New Orleans blues harmonica player, singer,\n"
            "and multi-instrumentalist who studied under James Cotton and\n"
            "Jr. Wells and toured with John Lee Hooker. Guitarist John Fohl\n"
            "was a founding member of the Cherry-Poppin' Daddies and worked\n"
            "extensively with Dr. John. Together, their deep-blues duo and\n"
            "trio configurations deliver raw Louisiana grit distilled from\n"
            "decades of Crescent City nightlife."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.johnnysansone.com"],
    ),
    # ── New Orleans Jazz National Historical Park Stage ────────────────
    Act(
        "Congo Square Preservation Society",
        JAZZPARK,
        SAT,
        t(11, 0),
        t(12, 0),
        genre=Genre.WORLD,
        about=(
            "Founded by percussionist Luther Gray, the Congo Square Preservation\n"
            "Society carries on the African drumming and dancing tradition of\n"
            "Congo Square \u2014 the historic site where enslaved people gathered on\n"
            "Sundays, planting seeds that grew into jazz, second line, and Mardi\n"
            "Gras Indian culture. Every Sunday they host drum circles in the\n"
            "park, and at FQF their performance is a communal, rhythmic\n"
            "experience rooted in centuries of tradition."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.congosquarepreservationsociety.org"],
    ),
    Act(
        "Jamil Sharif Quartet",
        JAZZPARK,
        SAT,
        t(12, 15),
        t(13, 15),
        genre=Genre.JAZZ_CONTEMPORARY,
        about=(
            "Born and raised in New Orleans, trumpeter Jamil Sharif began his\n"
            "studies with the same teacher who mentored Wynton Marsalis and\n"
            "Terence Blanchard. He has performed with the Lincoln Center Jazz\n"
            "Orchestra under Marsalis and recorded Portraits of New Orleans\n"
            "with Dr. John. His quartet navigates jazz, blues, swing, Latin,\n"
            "and funk with the effortless versatility of a true Crescent City\n"
            "musician."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["http://www.jamilsharif.com"],
    ),
    Act(
        "Shake Em Up Jazz Band",
        JAZZPARK,
        SAT,
        t(13, 30),
        t(14, 30),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "The Shake Em Up Jazz Band is an all-female cast of traditional\n"
            "New Orleans jazz musicians assembled by Shaye Cohn in 2016 for a\n"
            "Girls Rock New Orleans performance. The six-piece immediately\n"
            "garnered attention and now performs at Preservation Hall, Jazz Fest,\n"
            "and FQF. Their album A Woman's Place features songs exclusively\n"
            "from women composers of the 1910s through 1930s."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://shakeemupjazzband.com"],
    ),
    Act(
        "Young Tuxedo Brass Band",
        JAZZPARK,
        SAT,
        t(14, 45),
        t(15, 45),
        genre=Genre.BRASS_BAND,
        about=(
            "Founded in 1938 by John Casimir and named in tribute to Papa\n"
            "Celestin's Tuxedo Brass Band, the Young Tuxedo Brass Band is\n"
            "one of the last traditional New Orleans brass bands still playing\n"
            "the hymns, dirges, and songs of the original brass repertoire.\n"
            "Led by trumpeter Gregg Stafford since 1984, they first recorded\n"
            "for Atlantic Records in 1958 with Paul Barbarin on drums."
        ),
        about_source=AboutSource.RESEARCHED,
    ),
    Act(
        "Saskia Walker Big Band",
        JAZZPARK,
        SAT,
        t(16, 0),
        t(17, 0),
        genre=Genre.JAZZ_CONTEMPORARY,
        about=(
            "Originally from Italy, vocalist Saskia Walker leads her Little Big\n"
            "Band at the New Orleans Jazz National Historical Park, featuring\n"
            "an all-star lineup including drummer Willie Green III and pianist\n"
            "Victor Campbell. The ensemble delivers swinging standards and\n"
            "original arrangements that reflect the full spectrum of New\n"
            "Orleans jazz, from traditional to contemporary."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.saskiasmusic.com"],
    ),
    # ── Ernie's Schoolhouse Stage ─────────────────────────────────────
    Act(
        "Lyc\u00e9e Fran\u00e7ais Musicians",
        SCHOOLHOUSE,
        SAT,
        t(11, 0),
        t(12, 0),
        genre=Genre.MIXED_ECLECTIC,
        about=(
            "Student musicians from Lyc\u00e9e Fran\u00e7ais de la Nouvelle-Orl\u00e9ans\n"
            "showcase the school's music program on the Schoolhouse Stage."
        ),
        about_source=AboutSource.GENERATED,
    ),
    Act(
        "Pierre A Capdau Marching Jaguars",
        SCHOOLHOUSE,
        SAT,
        t(12, 20),
        t(13, 20),
        genre=Genre.BRASS_BAND,
        about=(
            "The Marching Jaguars from Pierre A. Capdau School bring youthful\n"
            "energy and New Orleans marching-band tradition to the Schoolhouse\n"
            "Stage."
        ),
        about_source=AboutSource.GENERATED,
    ),
    Act(
        "McMain Singing Mustangs",
        SCHOOLHOUSE,
        SAT,
        t(13, 50),
        t(14, 50),
        genre=Genre.GOSPEL,
        about=(
            "The Singing Mustangs from Eleanor McMain Secondary School perform\n"
            "choral music showcasing the vocal talent nurtured in New Orleans\n"
            "public schools."
        ),
        about_source=AboutSource.GENERATED,
    ),
    Act(
        "The Roots of Music",
        SCHOOLHOUSE,
        SAT,
        t(15, 10),
        t(16, 10),
        genre=Genre.BRASS_BAND,
        about=(
            "The Roots of Music is a nonprofit youth marching band and music\n"
            "education program founded in New Orleans to mentor young musicians\n"
            "in the city's brass-band tradition. Their performances showcase\n"
            "the next generation of New Orleans musical culture."
        ),
        about_source=AboutSource.GENERATED,
    ),
    Act(
        "Audubon Charter School R&B Choir",
        SCHOOLHOUSE,
        SAT,
        t(16, 30),
        t(17, 30),
        genre=Genre.RNB_SOUL,
        about=(
            "The R&B Choir from Audubon Charter School brings soulful vocal\n"
            "performances to the Schoolhouse Stage, highlighting the vibrant\n"
            "music programs in New Orleans' charter schools."
        ),
        about_source=AboutSource.GENERATED,
    ),
    # ── Hancock Whitney Stage ─────────────────────────────────────────
    Act(
        "Clive Wilson's New Orleans Serenaders",
        HANCOCK,
        SAT,
        t(11, 30),
        t(12, 45),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "British-born trumpeter Clive Wilson moved to New Orleans in 1964\n"
            "to study under seminal figures like Kid Howard and DeDe Pierce.\n"
            "His Serenaders \u2014 including clarinetist Tommy Sancton and pianist\n"
            "Butch Thompson \u2014 revive repertoire from Kid Ory, Louis Armstrong,\n"
            "and Jelly Roll Morton with the warmth of decades-long musical\n"
            "friendships forged in jam sessions, parades, and jazz funerals."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.clivewilsonmusic.com"],
    ),
    Act(
        "Caleb Tokarska",
        HANCOCK,
        SAT,
        t(13, 0),
        t(14, 15),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "Born in Augusta, Georgia and raised on the Grateful Dead, the\n"
            "Allman Brothers, The Meters, and James Brown, Caleb Tokarska\n"
            "moved to New Orleans in 2019 and quickly established himself\n"
            "through an appearance at Jazz Fest with John Boutte. His heartfelt\n"
            "guitar playing and powerful storytelling range from country to\n"
            "funk, exploring the full breadth of American roots music."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.instagram.com/calebtokarska/"],
    ),
    Act(
        "John Mahoney Little Band",
        HANCOCK,
        SAT,
        t(14, 30),
        t(15, 45),
        genre=Genre.JAZZ_CONTEMPORARY,
        about=(
            "John Mahoney is a native New Yorker who grew up on Glenn Miller\n"
            "and Count Basie and made New Orleans his home, eventually becoming\n"
            "Professor Emeritus of Jazz Studies at Loyola University. His Little\n"
            "Band delivers Great American Songbook classics arranged for\n"
            "listeners and dancers, seamlessly blending tradition and\n"
            "innovation. From solo piano to jazz quartet, every configuration\n"
            "swings."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.mahoneymusic.com"],
    ),
    Act(
        "Steve Pistorius & the Southern Syncopators",
        HANCOCK,
        SAT,
        t(16, 0),
        t(17, 15),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Steve Pistorius is the only living New Orleanian who specializes in\n"
            "early jazz piano, with a particular love for Jelly Roll Morton. He\n"
            "named the Southern Syncopators after Hurricane Katrina and has since\n"
            "built a repertoire spanning the New Orleans revival, Sidney Bechet,\n"
            "Clarence Williams, and Sam Morgan. A regular at Preservation Hall,\n"
            "he has recorded with Wynton Marsalis, Bob Wilber, and many others."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.stevepistorius.com"],
    ),
    # ── Omni Royal Orleans Stage ──────────────────────────────────────
    Act(
        "Garden District Jazz Band",
        OMNI,
        SAT,
        t(11, 15),
        t(12, 30),
        genre=Genre.JAZZ_CONTEMPORARY,
        about=(
            "Led by drummer David Hansen since 1994, the Garden District Jazz\n"
            "Band held an eighteen-year nightly residency at Houston's on\n"
            "St. Charles Avenue. The trio performs the Classic American Songbook\n"
            "with swing, bossa nova, samba, and a unique New Orleans feel on a\n"
            "seven-foot Steinway. They have played internationally in Argentina,\n"
            "Brazil, Japan, Malaysia, and Turkey."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://gardendistrictband.com"],
    ),
    Act(
        "Marlon Jordan and Quartet",
        OMNI,
        SAT,
        t(12, 45),
        t(14, 0),
        genre=Genre.JAZZ_CONTEMPORARY,
        about=(
            "Trumpeter Marlon Jordan was one of the 'Young Jazz Lions' signed\n"
            "to a major label in the 1980s, joining Wynton Marsalis and Miles\n"
            "Davis as a headlining act at JVC Festivals. The son of saxophonist\n"
            "Kidd Jordan and a graduate of NOCCA, he draws comparisons to\n"
            "Charlie Parker and Coltrane. His true joy remains performing\n"
            "in the streets and nightclubs of his hometown."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.marlonjordanmusic.com"],
    ),
    Act(
        "Louis Michot and Swamp Magic",
        OMNI,
        SAT,
        t(14, 15),
        t(15, 30),
        genre=Genre.CAJUN,
        about=(
            "Louis Michot is the fiddle player and lead singer of the Grammy-\n"
            "winning Lost Bayou Ramblers. Swamp Magic is his solo-adjacent\n"
            "project channeling psychedelic Cajun sounds, with a passion for\n"
            "Louisiana French, local folklore, and the disappearing wetlands\n"
            "of Acadiana. His solo album Reve du Troubadour features Nigerian\n"
            "Tuareg guitarist Bombino and cellist Leyla McCalla."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://lostbayouramblers.com"],
    ),
    Act(
        "The Crybabies",
        OMNI,
        SAT,
        t(15, 45),
        t(17, 0),
        genre=Genre.SINGER_SONGWRITER,
        about=(
            "Five fearsome ladies out of New Orleans singing their little hearts\n"
            "out in four-part harmony \u2014 The Crybabies deliver swooping, pristine\n"
            "folk songs with bright guitars, banjo, violin, and soothing\n"
            "melodies. The all-female band blends Americana, folk, and\n"
            "traditional-music influences into a sound that is equal parts\n"
            "tender and spirited."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://thecrybabies.bandcamp.com"],
    ),
    # ── KREWE Eyewear Stage ───────────────────────────────────────────
    Act(
        "Bad Penny Pleasuremakers",
        KREWE,
        SAT,
        t(11, 0),
        t(12, 15),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Matt Bell and Joy Patterson met on a blind date after Hurricane\n"
            "Katrina and have been making music together ever since. The Bad\n"
            "Penny Pleasuremakers offer Louisiana-drenched traditional jazz,\n"
            "ragtime, and acoustic and country blues from the pre-WWII era,\n"
            "all made for dancing. Their albums include T'aint No Sin and\n"
            "Hello Bluebird!"
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://badpennypleasuremakers.bandcamp.com"],
    ),
    Act(
        "Washboard Chaz Blues Trio",
        KREWE,
        SAT,
        t(12, 30),
        t(13, 45),
        genre=Genre.BLUES,
        about=(
            "Washboard Chaz, harmonica ace Andy J. Forest, and guitarist\n"
            "Jonathan Freilich form a Trio that covers delta, Piedmont, and\n"
            "Chicago blues with acoustic instruments and raw energy. Featured\n"
            "on HBO's Treme and named Offbeat's Best Emerging Blues Band in\n"
            "2004, Chaz has shared stages with Bonnie Raitt, Taj Mahal, and\n"
            "John Hammond. Their sets are a festival highlight for blues\n"
            "purists."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://www.washboardchaz.com"],
    ),
    Act(
        "Nanci Zhang",
        KREWE,
        SAT,
        t(14, 0),
        t(15, 15),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Nanci Zhang is a New Orleans vocalist who brings sensitivity,\n"
            "percussiveness, humor, and unmistakable warmth to the Great\n"
            "American Songbook. A listener first and performer second, her\n"
            "phrasing evokes the pianists she idolizes, and her voice recalls\n"
            "an earlier era of jazz singing. Off stage she is a registered\n"
            "nurse and public health advocate."
        ),
        about_source=AboutSource.RESEARCHED,
    ),
    Act(
        "Aurora Nealand & the Royal Roses",
        KREWE,
        SAT,
        t(15, 30),
        t(16, 45),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Saxophonist, clarinetist, and vocalist Aurora Nealand founded the\n"
            "Royal Roses in 2010, drawing heavily on Sidney Bechet and Django\n"
            "Reinhardt while routing collective improvisation through avant-garde\n"
            "and sound-art sensibilities. An Oberlin Conservatory graduate, she\n"
            "has performed at Montreal Jazz, Istanbul Jazz, and Lincoln Center.\n"
            "The Big Easy Awards named her Best Female Performer in 2016 and\n"
            "the Royal Roses Best Traditional Jazz Band in 2015 and 2017."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["http://www.auroranealand.com"],
    ),
    # ── Cafe Beignet Stage ────────────────────────────────────────────
    Act(
        "The Beignet Orchestra",
        CAFEBEIGNET,
        SAT,
        t(11, 30),
        t(14, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "The Beignet Orchestra of New Orleans performs daily at the Cafe\n"
            "Beignet on Bourbon Street, led by trombonist, harmonica player,\n"
            "and singer Dave Ruffner. The ensemble blends Dixieland jazz, big\n"
            "band, and mainstream jazz into a warm, accessible show that is\n"
            "the perfect musical accompaniment to a plate of beignets and\n"
            "a cup of cafe au lait."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://daveruffnermusic.com"],
    ),
    Act(
        "Zach Wiggins Trio",
        CAFEBEIGNET,
        SAT,
        t(14, 30),
        t(17, 0),
        genre=Genre.JAZZ_TRADITIONAL,
        about=(
            "Dr. Zachary Wiggins is a pianist, singer, arranger, and educator\n"
            "who wrote his doctorate on teaching New Orleans jazz in college\n"
            "programs. His trio delivers traditional jazz piano styles with\n"
            "scholarly depth and genuine swing. He also directs The Nash Summer\n"
            "Trad Jazz Workshop, passing the tradition to the next generation\n"
            "of players."
        ),
        about_source=AboutSource.RESEARCHED,
        websites=["https://drzachwiggins.com"],
    ),
]
