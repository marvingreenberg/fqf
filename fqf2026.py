"""
French Quarter Festival 2026 - Schedule Data & Query API
Dates: April 17-20, 2026
"""

from datetime import date, time, datetime
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Act:
    name: str
    stage: str
    date: date
    start: time
    end: time

    def as_tuple(self):
        return (self.name, self.stage, self.start.strftime("%-I:%M %p"), self.end.strftime("%-I:%M %p"))

    def __str__(self):
        return (f"{self.name:<60} | {self.stage:<45} | "
                f"{self.date.strftime('%a %b %d')} | "
                f"{self.start.strftime('%-I:%M %p')} - {self.end.strftime('%-I:%M %p')}")


def t(h, m):
    return time(h, m)

THU = date(2026, 4, 16)
FRI = date(2026, 4, 17)
SAT = date(2026, 4, 18)
SUN = date(2026, 4, 19)

ABITA         = "Abita Beer Stage"
NEWORLEANS    = "NewOrleans.com Stage"
TROPICAL      = "Tropical Isle Hand Grenade Stage"
JACKDANIELS   = "Jack Daniel's Stage"
WILLOW        = "Willow Dispensary Stage"
LOYOLA        = "Loyola Esplanade in the Shade Stage"
FISHFRY       = "Louisiana Fish Fry Stage"
ENTERGY       = "Entergy Songwriter Stage"
PANAMLIFE     = "Pan-American Life Insurance Group Stage"
JAZZPLAYHOUSE = "Jazz Playhouse at the Royal Sonesta"
FRENCHMARKET  = "French Market Traditional Jazz Stage"
DUTCHALLEY    = "French Market Dutch Alley Stage"
HOUSEOFBLUES  = "House of Blues Voodoo Garden Stage"
JAZZPARK      = "New Orleans Jazz National Historical Park Stage"
SCHOOLHOUSE   = "Ernie's Schoolhouse Stage"
HANCOCK       = "Hancock Whitney Stage"
OMNI          = "Omni Royal Orleans Stage"
KREWE         = "KREWE Eyewear Stage"
CAFEBEIGNET   = "Cafe Beignet Stage"


SCHEDULE = [
    # ── THURSDAY April 17 ──────────────────────────────────────────────────
    Act("Seguenon Kone featuring Ivorie Spectacle",          ABITA,         THU, t(11,30), t(12,30)),
    Act("The Quickening",                                    ABITA,         THU, t(12,50), t(13,50)),
    Act("Kermit Ruffins & the Barbecue Swingers",           ABITA,         THU, t(14,10), t(15,10)),
    Act("Big Chief Juan Pardo's Tribal Gold",                ABITA,         THU, t(15,30), t(16,30)),
    Act("Erica Falls & Vintage Soul",                        ABITA,         THU, t(16,50), t(18,10)),
    Act("The Soul Rebels",                                   ABITA,         THU, t(18,40), t(20, 0)),

    Act("Preservation Brass",                                NEWORLEANS,    THU, t(11,15), t(12,25)),
    Act("Banu Gibson",                                       NEWORLEANS,    THU, t(12,45), t(14, 0)),
    Act("Mahogany Hall All Stars Band",                      NEWORLEANS,    THU, t(14,20), t(15,30)),
    Act("Leroy Jones & New Orleans' Finest",                 NEWORLEANS,    THU, t(15,50), t(17,10)),
    Act("The Lilli Lewis Project",                           NEWORLEANS,    THU, t(17,30), t(18,45)),

    Act("Mem Shannon & The Membership",                      TROPICAL,      THU, t(11,10), t(12,10)),
    Act("Sir Chantz Powell & The Sound Of Funk (S.O.F.)",   TROPICAL,      THU, t(12,30), t(13,30)),
    Act("Susan Cowsill",                                     TROPICAL,      THU, t(13,50), t(14,50)),
    Act("Yusa & Mahmoud Chouki",                             TROPICAL,      THU, t(15,10), t(16,10)),
    Act("Royal Essence",                                     TROPICAL,      THU, t(16,30), t(17,45)),
    Act("Bag of Donuts",                                     TROPICAL,      THU, t(18,15), t(19,45)),

    Act("R & R Smokin' Foundation",                          JACKDANIELS,   THU, t(11,10), t(12,30)),
    Act("Bon Bon Vivant",                                    JACKDANIELS,   THU, t(12,50), t(13,50)),
    Act("Juice",                                             JACKDANIELS,   THU, t(14,10), t(15,10)),
    Act("Sierra Green and the Giants",                       JACKDANIELS,   THU, t(15,30), t(16,40)),
    Act("Rebirth Brass Band",                                JACKDANIELS,   THU, t(17, 0), t(18,20)),
    Act("Bobby Rush",                                        JACKDANIELS,   THU, t(18,50), t(20, 0)),

    Act("T'Monde",                                           WILLOW,        THU, t(11,10), t(12,20)),
    Act("Gerard Delafose and The Zydeco Gators",             WILLOW,        THU, t(12,40), t(13,50)),
    Act("Waylon Thibodeaux Band",                            WILLOW,        THU, t(14,10), t(15,10)),
    Act("Nathan and the Zydeco Cha Chas",                    WILLOW,        THU, t(15,30), t(16,40)),
    Act("Amanda Shaw",                                       WILLOW,        THU, t(17, 0), t(18,10)),
    Act("Johnny Sketch and the Dirty Notes",                 WILLOW,        THU, t(18,45), t(20, 0)),

    Act("Red Hot Brass Band",                                FISHFRY,       THU, t(11,10), t(12,30)),
    Act("504 Millz",                                         FISHFRY,       THU, t(12,35), t(13, 5)),
    Act("J.A.M. Brass Band",                                 FISHFRY,       THU, t(13,10), t(14,30)),
    Act("Zeus",                                              FISHFRY,       THU, t(14,35), t(15,15)),
    Act("SOUL Brass Band",                                   FISHFRY,       THU, t(15,20), t(16,40)),
    Act("DJ Legatron Prime",                                 FISHFRY,       THU, t(16,45), t(17,30)),
    Act("New Orleans Nightcrawlers",                         FISHFRY,       THU, t(17,35), t(18,55)),
    Act("Raj Smoove",                                        FISHFRY,       THU, t(19, 0), t(20, 0)),

    Act("Gal Holiday and the Honky Tonk Revue",              PANAMLIFE,     THU, t(11, 0), t(12,10)),
    Act("The Tin Men",                                       PANAMLIFE,     THU, t(12,30), t(13,30)),
    Act("T-Ray & The Trendsetters",                          PANAMLIFE,     THU, t(13,50), t(14,50)),
    Act("Muévelo",                                           PANAMLIFE,     THU, t(15,10), t(16,10)),
    Act("John Mooney",                                       PANAMLIFE,     THU, t(16,30), t(17,50)),
    Act("The New Orleans Klezmer All Stars",                 PANAMLIFE,     THU, t(18,10), t(19,30)),

    Act("Jake Landry",                                       HOUSEOFBLUES,  THU, t(12,30), t(14,30)),
    Act("Funky Lampshades",                                  HOUSEOFBLUES,  THU, t(15, 0), t(17, 0)),
    Act("Cary Hudson",                                       HOUSEOFBLUES,  THU, t(17,30), t(19,30)),
    Act("Julian Primeaux",                                   HOUSEOFBLUES,  THU, t(19,30), t(21,30)),

    # ── FRIDAY April 18 ────────────────────────────────────────────────────
    Act("Bo Dollis Jr. and the Wild Magnolias",              ABITA,         FRI, t(11,30), t(12,30)),
    Act("Irvin Mayfield",                                    ABITA,         FRI, t(12,50), t(13,50)),
    Act("The Dixie Cups",                                    ABITA,         FRI, t(14,10), t(15,10)),
    Act("Bonerama",                                          ABITA,         FRI, t(15,30), t(16,30)),
    Act("Jon Cleary & the Absolute Monster Gentlemen",       ABITA,         FRI, t(16,50), t(18,10)),
    Act("PJ Morton",                                         ABITA,         FRI, t(18,40), t(20, 0)),

    Act("John Boutté",                                       NEWORLEANS,    FRI, t(11,15), t(12,25)),
    Act("Don Vappie and the Creole Jazz Serenaders",         NEWORLEANS,    FRI, t(12,45), t(14, 0)),
    Act("Lawrence Cotton Legendary Experience",               NEWORLEANS,    FRI, t(14,20), t(15,30)),
    Act("Kyle Roussel's Church of New Orleans",              NEWORLEANS,    FRI, t(15,50), t(17, 0)),
    Act("Robin Barnes & The Fiya Birds",                     NEWORLEANS,    FRI, t(17,20), t(18,45)),

    Act("Maji Melodies - Semaj & The Blues Experiment",      TROPICAL,      FRI, t(11,10), t(12,10)),
    Act("Joe Lastie's Jazz to Brass feat. Dr. Pathorn",      TROPICAL,      FRI, t(12,30), t(13,30)),
    Act("Ashton Hines and the Big Easy Brawlers",            TROPICAL,      FRI, t(13,50), t(14,50)),
    Act("Sally Baby's Silver Dollars",                       TROPICAL,      FRI, t(15,10), t(16,10)),
    Act("Deezle",                                            TROPICAL,      FRI, t(16,30), t(17,45)),
    Act("Lisa Amos",                                         TROPICAL,      FRI, t(18,15), t(19,45)),

    Act("Khris Royal and Dark Matter",                       JACKDANIELS,   FRI, t(11,10), t(12,30)),
    Act("Cole Williams",                                     JACKDANIELS,   FRI, t(12,50), t(13,50)),
    Act("The Iguanas",                                       JACKDANIELS,   FRI, t(14,10), t(15,10)),
    Act("People Museum",                                     JACKDANIELS,   FRI, t(15,30), t(16,40)),
    Act("LSD Clown System",                                  JACKDANIELS,   FRI, t(17, 0), t(18,20)),
    Act("The Dirty Dozen Brass Band",                        JACKDANIELS,   FRI, t(18,50), t(20, 0)),

    Act("T Marie and Bayou Juju",                            WILLOW,        FRI, t(11,10), t(12,20)),
    Act("T'Canaille",                                        WILLOW,        FRI, t(12,40), t(13,50)),
    Act("B. Cam & The Zydeco Young Bucks",                  WILLOW,        FRI, t(14,10), t(15,10)),
    Act("Lost Bayou Ramblers",                               WILLOW,        FRI, t(15,30), t(16,40)),
    Act("Sunpie and the Louisiana Sunspots",                 WILLOW,        FRI, t(17, 0), t(18,10)),
    Act("Brass-A-Holics",                                    WILLOW,        FRI, t(18,40), t(20, 0)),

    Act("Kirkland Green",                                    LOYOLA,        FRI, t(11, 0), t(12, 0)),
    Act("Tuller, Not Related, Liam Escame, and Surco",       LOYOLA,        FRI, t(12,20), t(13,35)),
    Act("The RiverBenders",                                  LOYOLA,        FRI, t(13,55), t(14,50)),
    Act("Pellow Talk & Alfred Banks",                        LOYOLA,        FRI, t(15,10), t(16,10)),
    Act("New Orleans Legacy Coalition",                      LOYOLA,        FRI, t(16,30), t(17,30)),
    Act("Cha Wa",                                            LOYOLA,        FRI, t(17,50), t(19, 0)),

    Act("Magnetic Ear",                                      FISHFRY,       FRI, t(11,10), t(12,20)),
    Act("Tidal Wave Brass Band",                             FISHFRY,       FRI, t(12,40), t(14, 0)),
    Act("DJ ChiNola",                                        FISHFRY,       FRI, t(14, 5), t(14,35)),
    Act("Young Pinstripe Brass Band",                        FISHFRY,       FRI, t(14,40), t(16, 0)),
    Act("Kidd Love",                                         FISHFRY,       FRI, t(16, 5), t(16,35)),
    Act("Treme Brass Band",                                  FISHFRY,       FRI, t(16,40), t(17,45)),
    Act("DJ Polo504",                                        FISHFRY,       FRI, t(17,50), t(18,35)),
    Act("Sporty's Brass Band",                               FISHFRY,       FRI, t(18,40), t(20, 0)),

    Act("Don Paul and Rivers Answer Moons",                  ENTERGY,       FRI, t(11, 0), t(11,55)),
    Act("Lisbon Girls",                                      ENTERGY,       FRI, t(12,15), t(13,10)),
    Act("Kelly Love Jones",                                  ENTERGY,       FRI, t(13,30), t(14,25)),
    Act("Johnny Sansone",                                    ENTERGY,       FRI, t(14,45), t(15,40)),
    Act("Max Bien-Kahn",                                     ENTERGY,       FRI, t(16, 0), t(17, 0)),

    Act("Lulu and the Broadsides",                           PANAMLIFE,     FRI, t(11, 0), t(12,10)),
    Act("Arsène Delay & Charlie Wooton",                    PANAMLIFE,     FRI, t(12,30), t(13,30)),
    Act("Dusky Waters",                                      PANAMLIFE,     FRI, t(13,50), t(14,50)),
    Act("Amigos do Samba",                                   PANAMLIFE,     FRI, t(15,10), t(16,10)),
    Act("Camile Baudoin and Friends",                        PANAMLIFE,     FRI, t(16,30), t(17,20)),
    Act("Bill Summers & Jazalsa",                            PANAMLIFE,     FRI, t(18,10), t(19,30)),

    Act("The Sam Lobley Band",                               JAZZPLAYHOUSE, FRI, t(11, 0), t(13,30)),
    Act("Antoine Diel & New Orleans Misfit Power Band",      JAZZPLAYHOUSE, FRI, t(14, 0), t(16,30)),
    Act("Chucky C & Friends",                                JAZZPLAYHOUSE, FRI, t(17, 0), t(19,30)),

    Act("Panorama Jazz Band",                                FRENCHMARKET,  FRI, t(11,30), t(13, 0)),
    Act("Rickie Monie & the Traditional Jazz Ramblers",      FRENCHMARKET,  FRI, t(13,30), t(15, 0)),
    Act("The New Orleans Flairs",                            FRENCHMARKET,  FRI, t(15,30), t(17, 0)),
    Act("Ingrid Lucia",                                      FRENCHMARKET,  FRI, t(17,30), t(19, 0)),

    Act("Tyler Twerk Thomson",                               DUTCHALLEY,    FRI, t(11,15), t(12,30)),
    Act("Palmetto Bug Stompers",                             DUTCHALLEY,    FRI, t(12,45), t(14, 0)),
    Act("The Pfister Sisters",                               DUTCHALLEY,    FRI, t(14,15), t(15,30)),
    Act("New Orleans Classic Jazz Orchestra",                DUTCHALLEY,    FRI, t(15,45), t(17, 0)),

    Act("Shawan Rice Trio",                                  HOUSEOFBLUES,  FRI, t(11,15), t(12,30)),
    Act("Joey Houcke",                                       HOUSEOFBLUES,  FRI, t(12,45), t(14,45)),
    Act("Electric Ramble",                                   HOUSEOFBLUES,  FRI, t(15, 0), t(17, 0)),
    Act("Borders Trio",                                      HOUSEOFBLUES,  FRI, t(17,15), t(19,15)),
    Act("Tanglers",                                          HOUSEOFBLUES,  FRI, t(19,30), t(21,30)),

    # ── SATURDAY April 19 ──────────────────────────────────────────────────
    Act("Gregg Martinez & the Delta Kings",                  ABITA,         SAT, t(11,30), t(12,30)),
    Act("Ryan Batiste and Raw Revolution",                   ABITA,         SAT, t(12,50), t(13,50)),
    Act("Big Chief Monk Boudreaux and the Golden Eagles",    ABITA,         SAT, t(14,10), t(15,10)),
    Act("Dawn Richard",                                      ABITA,         SAT, t(15,30), t(16,30)),
    Act("George Porter Jr & Runnin' Pardners",               ABITA,         SAT, t(17, 0), t(18,20)),
    Act("Flow Tribe",                                        ABITA,         SAT, t(18,40), t(20, 0)),

    Act("Tim Laughlin",                                      NEWORLEANS,    SAT, t(11,15), t(12,35)),
    Act("The Big Easy Boys",                                 NEWORLEANS,    SAT, t(12,45), t(14, 0)),
    Act("Wendell Brunious",                                  NEWORLEANS,    SAT, t(14,20), t(15,30)),
    Act("Charmaine Neville",                                 NEWORLEANS,    SAT, t(15,50), t(17, 0)),
    Act("James Andrews",                                     NEWORLEANS,    SAT, t(17,20), t(18,45)),

    Act("Christian Serpas & Ghost Town",                     TROPICAL,      SAT, t(11,10), t(12,10)),
    Act("Ovi-G presents 'Xtra Cash!'",                       TROPICAL,      SAT, t(12,30), t(13,30)),
    Act("Ronnie Lamarque Orchestra feat. Hot Rod Lincoln",   TROPICAL,      SAT, t(14, 0), t(15,15)),
    Act("Victor Campbell & Timba Swamp",                     TROPICAL,      SAT, t(15,35), t(16,35)),
    Act("Flagboy Giz & the Wild Tchoupitoulas",              TROPICAL,      SAT, t(16,55), t(17,55)),
    Act("Higher Heights Reggae Band",                        TROPICAL,      SAT, t(18,15), t(19,45)),

    Act("Lily Unless and The If Onlys",                      JACKDANIELS,   SAT, t(11,10), t(12,30)),
    Act("Paul Sanchez",                                      JACKDANIELS,   SAT, t(12,50), t(13,50)),
    Act("Water Seed",                                        JACKDANIELS,   SAT, t(14,10), t(15,10)),
    Act("Iceman Special",                                    JACKDANIELS,   SAT, t(15,30), t(16,40)),
    Act("The Original Pinettes Brass Band",                  JACKDANIELS,   SAT, t(17, 0), t(18,20)),
    Act("Big Freedia",                                       JACKDANIELS,   SAT, t(18,50), t(20, 0)),

    Act("Bruce Daigrepont Cajun Band",                       WILLOW,        SAT, t(11,10), t(12,20)),
    Act("Magnolia Sisters",                                  WILLOW,        SAT, t(12,40), t(13,50)),
    Act("Donna Angelle & the Zydeco Posse",                  WILLOW,        SAT, t(14,10), t(15,10)),
    Act("Corey Ledet Zydeco & Black Magic",                  WILLOW,        SAT, t(15,30), t(16,40)),
    Act("Dwayne Dopsie and the Zydeco Hellraisers",          WILLOW,        SAT, t(17, 0), t(18,10)),
    Act("Sweet Crude",                                       WILLOW,        SAT, t(18,30), t(20, 0)),

    Act("Loyola University Commercial Ensemble",             LOYOLA,        SAT, t(11, 0), t(12,15)),
    Act("Joy Clark",                                         LOYOLA,        SAT, t(12,35), t(13,45)),
    Act("Tay/Heavensworld/Ja Fierce & Azure Skye et al.",   LOYOLA,        SAT, t(14,10), t(15,30)),
    Act("Mia Borders",                                       LOYOLA,        SAT, t(15,50), t(17,10)),
    Act("John 'Papa' Gros",                                  LOYOLA,        SAT, t(17,30), t(19, 0)),

    Act("Red Wolf Brass Band",                               FISHFRY,       SAT, t(11,10), t(12,30)),
    Act("DJ Hollaback",                                      FISHFRY,       SAT, t(12,35), t(13, 5)),
    Act("Storyville Stompers Brass Band",                    FISHFRY,       SAT, t(13,10), t(14,30)),
    Act("DJ Spin",                                           FISHFRY,       SAT, t(14,35), t(15,15)),
    Act("Original Hurricane Brass Band",                     FISHFRY,       SAT, t(15,20), t(16,40)),
    Act("DJ RQ Away",                                        FISHFRY,       SAT, t(16,45), t(17,30)),
    Act("Big 6 Brass Band",                                  FISHFRY,       SAT, t(17,35), t(18,55)),
    Act("DJ Poppa",                                          FISHFRY,       SAT, t(19, 0), t(20, 0)),

    Act("John Rankin",                                       ENTERGY,       SAT, t(11, 0), t(11,55)),
    Act("Beth Patterson",                                    ENTERGY,       SAT, t(12,15), t(13,10)),
    Act("Kyle Alexander",                                    ENTERGY,       SAT, t(13,30), t(14,25)),
    Act("Daphne Parker Powell",                              ENTERGY,       SAT, t(14,45), t(15,45)),
    Act("AdoSoul and the Tribe",                             ENTERGY,       SAT, t(16, 5), t(17, 0)),

    Act("Legendary Barbara Shorts and Blue Jazz",            PANAMLIFE,     SAT, t(11, 0), t(12,10)),
    Act("Lynn Drury",                                        PANAMLIFE,     SAT, t(12,30), t(13,30)),
    Act("Vivaz",                                             PANAMLIFE,     SAT, t(13,50), t(14,50)),
    Act("Ever More Nest",                                    PANAMLIFE,     SAT, t(15,10), t(16,10)),
    Act("Troy Sawyer and the Elementz",                      PANAMLIFE,     SAT, t(16,30), t(17,50)),
    Act("Fermín Ceballos + Merengue4FOUR",                  PANAMLIFE,     SAT, t(18,10), t(19,30)),

    Act("Audrey Lecrone",                                    JAZZPLAYHOUSE, SAT, t(11, 0), t(13,30)),
    Act("The Wolfe Johns Blues Band",                        JAZZPLAYHOUSE, SAT, t(14, 0), t(16,30)),
    Act("Richard 'Piano' Scott & The Twisty River Band",    JAZZPLAYHOUSE, SAT, t(17, 0), t(19,30)),

    Act("Secret Six Jazz Band",                              FRENCHMARKET,  SAT, t(11,30), t(13, 0)),
    Act("Special Dance Performance by the NOLA Chorus Girls",FRENCHMARKET,  SAT, t(13, 0), t(13, 5)),
    Act("New Orleans Cottonmouth Kings",                     FRENCHMARKET,  SAT, t(13,30), t(15, 0)),
    Act("Alicia Renee aka Blue Eyes Sextet",                 FRENCHMARKET,  SAT, t(15,30), t(17, 0)),
    Act("The Jump Hounds",                                   FRENCHMARKET,  SAT, t(17,30), t(19, 0)),

    Act("Kid Simmons Jazz Band",                             DUTCHALLEY,    SAT, t(11,15), t(12,30)),
    Act("Stephen Walker N'Em Swinging in New Orleans",       DUTCHALLEY,    SAT, t(12,45), t(14, 0)),
    Act("Kevin Ray Clark and Bourbon Street All Stars",      DUTCHALLEY,    SAT, t(14,15), t(15,30)),
    Act("New Orleans Ragtime Orchestra ft. Lars Edegran",    DUTCHALLEY,    SAT, t(15,45), t(17, 0)),

    Act("Tiago Guy & Renee Gros",                            HOUSEOFBLUES,  SAT, t(11,15), t(12,30)),
    Act("Pocket Chocolate",                                  HOUSEOFBLUES,  SAT, t(12,45), t(14,45)),
    Act("Jamey St. Pierre",                                  HOUSEOFBLUES,  SAT, t(15, 0), t(17, 0)),
    Act("Eric Johanson",                                     HOUSEOFBLUES,  SAT, t(17,15), t(19,15)),
    Act("Sansone & John Fohl",                               HOUSEOFBLUES,  SAT, t(19,30), t(21,30)),

    Act("Congo Square Preservation Society",                 JAZZPARK,      SAT, t(11, 0), t(12, 0)),
    Act("Jamil Sharif Quartet",                              JAZZPARK,      SAT, t(12,15), t(13,15)),
    Act("Shake Em Up Jazz Band",                             JAZZPARK,      SAT, t(13,30), t(14,30)),
    Act("Young Tuxedo Brass Band",                           JAZZPARK,      SAT, t(14,45), t(15,45)),
    Act("Saskia Walker Big Band",                            JAZZPARK,      SAT, t(16, 0), t(17, 0)),

    Act("Lycée Français Musicians",                          SCHOOLHOUSE,   SAT, t(11, 0), t(12, 0)),
    Act("Pierre A Capdau Marching Jaguars",                  SCHOOLHOUSE,   SAT, t(12,20), t(13,20)),
    Act("McMain Singing Mustangs",                           SCHOOLHOUSE,   SAT, t(13,50), t(14,50)),
    Act("The Roots of Music",                                SCHOOLHOUSE,   SAT, t(15,10), t(16,10)),
    Act("Audubon Charter School R&B Choir",                  SCHOOLHOUSE,   SAT, t(16,30), t(17,30)),

    Act("Clive Wilson's New Orleans Serenaders",             HANCOCK,       SAT, t(11,30), t(12,45)),
    Act("Caleb Tokarska",                                    HANCOCK,       SAT, t(13, 0), t(14,15)),
    Act("John Mahoney Little Band",                          HANCOCK,       SAT, t(14,30), t(15,45)),
    Act("Steve Pistorius & the Southern Syncopators",        HANCOCK,       SAT, t(16, 0), t(17,15)),

    Act("Garden District Jazz Band",                         OMNI,          SAT, t(11,15), t(12,30)),
    Act("Marlon Jordan and Quartet",                         OMNI,          SAT, t(12,45), t(14, 0)),
    Act("Louis Michot and Swamp Magic",                      OMNI,          SAT, t(14,15), t(15,30)),
    Act("The Crybabies",                                     OMNI,          SAT, t(15,45), t(17, 0)),

    Act("Bad Penny Pleasuremakers",                          KREWE,         SAT, t(11, 0), t(12,15)),
    Act("Washboard Chaz Blues Trio",                         KREWE,         SAT, t(12,30), t(13,45)),
    Act("Nanci Zhang",                                       KREWE,         SAT, t(14, 0), t(15,15)),
    Act("Aurora Nealand & the Royal Roses",                  KREWE,         SAT, t(15,30), t(16,45)),

    Act("The Beignet Orchestra",                             CAFEBEIGNET,   SAT, t(11,30), t(14, 0)),
    Act("Zach Wiggins Trio",                                 CAFEBEIGNET,   SAT, t(14,30), t(17, 0)),

    # ── SUNDAY April 20 ────────────────────────────────────────────────────
    Act("Sam Price & the True Believers",                    ABITA,         SUN, t(11,30), t(12,30)),
    Act("Bucktown All-Stars",                                ABITA,         SUN, t(12,50), t(13,50)),
    Act("New Orleans Suspects",                              ABITA,         SUN, t(14,10), t(15,10)),
    Act("Jelly Joseph",                                      ABITA,         SUN, t(15,30), t(16,30)),
    Act("Hasizzle with TBC Brass Band",                      ABITA,         SUN, t(17, 0), t(18,20)),
    Act("Cyril Neville",                                     ABITA,         SUN, t(18,50), t(20, 0)),

    Act("Tuba Skinny",                                       NEWORLEANS,    SUN, t(11,15), t(12,25)),
    Act("Lena Prima",                                        NEWORLEANS,    SUN, t(12,45), t(14, 0)),
    Act("Jeremy Davenport",                                  NEWORLEANS,    SUN, t(14,20), t(15,30)),
    Act("Judith Owen & Her Gentlemen Callers",               NEWORLEANS,    SUN, t(15,50), t(17,10)),
    Act("Delfeayo Marsalis & the Uptown Jazz Orchestra",     NEWORLEANS,    SUN, t(17,30), t(18,45)),

    Act("Professor Craig Adams & the Higher Dimensions Band",TROPICAL,      SUN, t(11,10), t(12,10)),
    Act("Alex McMurray",                                     TROPICAL,      SUN, t(12,30), t(13,30)),
    Act("Assata Renay",                                      TROPICAL,      SUN, t(13,50), t(14,50)),
    Act("Wanda Rouzan and a Taste of New Orleans",           TROPICAL,      SUN, t(15,10), t(16,10)),
    Act("Big Frank & Lil Frank & the Dirty Old Men",         TROPICAL,      SUN, t(16,30), t(17,45)),
    Act("Honey Island Swamp Band",                           TROPICAL,      SUN, t(18,15), t(19,45)),

    Act("Roderick 'Rev' Paulin and The Congregation",        JACKDANIELS,   SUN, t(11,10), t(12,30)),
    Act("Jason Neville Funky Soul Allstar Band",             JACKDANIELS,   SUN, t(12,50), t(13,50)),
    Act("Gumbeaux Juice",                                    JACKDANIELS,   SUN, t(14,10), t(15,10)),
    Act("The Rumble featuring Chief Joseph Boudreaux Jr",    JACKDANIELS,   SUN, t(15,30), t(16,30)),
    Act("Irma Thomas, Soul Queen of New Orleans",            JACKDANIELS,   SUN, t(17, 0), t(18,10)),
    Act("Cupid & the Dance Party Express Band",              JACKDANIELS,   SUN, t(18,40), t(20, 0)),

    Act("Les Femmes Farouches",                              WILLOW,        SUN, t(11,10), t(12,20)),
    Act("Cameron Dupuy & the Cajun Troubadours",             WILLOW,        SUN, t(12,40), t(13,50)),
    Act("Yvette Landry & the Jukes",                         WILLOW,        SUN, t(14,10), t(15,10)),
    Act("Buckwheat Zydeco Jr. & The Legendary Ils Sont Partis Band", WILLOW, SUN, t(15,30), t(16,40)),
    Act("Chubby Carrier and the Bayou Swamp Band",           WILLOW,        SUN, t(17, 0), t(18,10)),
    Act("Rockin' Dopsie Jr. & the Zydeco Twisters",         WILLOW,        SUN, t(18,40), t(20, 0)),

    Act("Casme",                                             LOYOLA,        SUN, t(11, 0), t(12, 0)),
    Act("Across Phoenix, James Wyzten, Kissing Disease",     LOYOLA,        SUN, t(12,20), t(13,35)),
    Act("Kristin Diable",                                    LOYOLA,        SUN, t(13,55), t(14,50)),
    Act("Helen Gillet: ReBelle Musique",                     LOYOLA,        SUN, t(15,10), t(16,10)),
    Act("Creole String Beans",                               LOYOLA,        SUN, t(16,30), t(17,30)),
    Act("Astral Project",                                    LOYOLA,        SUN, t(17,50), t(19, 0)),

    Act("Smokin' on Some Brass",                             FISHFRY,       SUN, t(11,10), t(12,20)),
    Act("New Birth Brass Band",                              FISHFRY,       SUN, t(12,40), t(14, 0)),
    Act("DJ Vintage",                                        FISHFRY,       SUN, t(14, 5), t(14,35)),
    Act("Kings of Brass",                                    FISHFRY,       SUN, t(14,40), t(16, 0)),
    Act("DJ ODD Spinz",                                      FISHFRY,       SUN, t(16, 5), t(16,35)),
    Act("Hot 8 Brass Band",                                  FISHFRY,       SUN, t(16,40), t(17,45)),
    Act("ANTWIGADEE!",                                       FISHFRY,       SUN, t(17,50), t(18,35)),
    Act("New Breed",                                         FISHFRY,       SUN, t(18,40), t(20, 0)),

    Act("Andy J Forest Treeaux",                             ENTERGY,       SUN, t(11, 0), t(11,55)),
    Act("Luke Allen",                                        ENTERGY,       SUN, t(12,15), t(13,10)),
    Act("Justin Garner",                                     ENTERGY,       SUN, t(13,30), t(14,25)),
    Act("Bobbi Rae",                                         ENTERGY,       SUN, t(14,45), t(15,45)),
    Act("Cristina Kaminis",                                  ENTERGY,       SUN, t(16, 5), t(17, 0)),

    Act("Bamboula 2000",                                     PANAMLIFE,     SUN, t(11,10), t(12,10)),
    Act("Anaïs St. John",                                   PANAMLIFE,     SUN, t(12,30), t(13,30)),
    Act("Papo y Son Mandao",                                 PANAMLIFE,     SUN, t(13,50), t(14,50)),
    Act("Los Güiros",                                        PANAMLIFE,     SUN, t(15,10), t(16,10)),
    Act("Stanton Moore featuring Joe Ashlar and Danny Abel", PANAMLIFE,     SUN, t(16,30), t(17,50)),
    Act("Leyla McCalla",                                     PANAMLIFE,     SUN, t(18,10), t(19,30)),

    Act("Jenna McSwain Jazz Band",                           JAZZPLAYHOUSE, SUN, t(11, 0), t(13,30)),
    Act("Jeanne Marie Harris",                               JAZZPLAYHOUSE, SUN, t(14, 0), t(16,30)),
    Act("Gerald French & The Original Tuxedo Jazz Band",     JAZZPLAYHOUSE, SUN, t(17, 0), t(19,30)),

    Act("Smoking Time Jazz Club",                            FRENCHMARKET,  SUN, t(11,30), t(13, 0)),
    Act("Charlie Halloran and the Tropicales",               FRENCHMARKET,  SUN, t(13,30), t(15, 0)),
    Act("The New Orleans Swinging Gypsies",                  FRENCHMARKET,  SUN, t(15,30), t(17, 0)),
    Act("Sullivan Dabney's Muzik Jazz Band",                 FRENCHMARKET,  SUN, t(17,30), t(19, 0)),

    Act("Hot Club of New Orleans",                           DUTCHALLEY,    SUN, t(11,15), t(12,30)),
    Act("Mayumi Shara & New Orleans Jazz Letters",           DUTCHALLEY,    SUN, t(12,45), t(14, 0)),
    Act("Jade Perdue",                                       DUTCHALLEY,    SUN, t(14,15), t(15,30)),
    Act("Tom Saunders and the Hotcats",                      DUTCHALLEY,    SUN, t(15,45), t(17, 0)),

    Act("Sophia Parigi",                                     HOUSEOFBLUES,  SUN, t(12,30), t(14,30)),
    Act("Sean Riley",                                        HOUSEOFBLUES,  SUN, t(15, 0), t(17, 0)),

    Act("Craig Klein's New Orleans Allstars",                JAZZPARK,      SUN, t(11, 0), t(12, 0)),
    Act("Matt Lemmler presents 'New Orleans in Stride'",     JAZZPARK,      SUN, t(12,15), t(13,15)),
    Act("Crescent City Sisters",                             JAZZPARK,      SUN, t(13,30), t(14,30)),
    Act("Louis Ford",                                        JAZZPARK,      SUN, t(14,45), t(15,45)),
    Act("Arrowhead Jazz Band feat. NPS Rangers et al.",      JAZZPARK,      SUN, t(16, 0), t(17, 0)),

    Act("Greater New Orleans Youth Orchestras",              SCHOOLHOUSE,   SUN, t(11, 0), t(12, 0)),
    Act("Chalmette High School Marching Band",               SCHOOLHOUSE,   SUN, t(12,20), t(13,20)),
    Act("St. Mary's Academy Gospel Choir",                   SCHOOLHOUSE,   SUN, t(13,50), t(14,50)),
    Act("Don Jamison Heritage School of Music",              SCHOOLHOUSE,   SUN, t(15,10), t(16,10)),
    Act("Walter L. Cohen High School Marching Band",         SCHOOLHOUSE,   SUN, t(16,30), t(17,30)),

    Act("Kid Merv & All That Jazz",                          HANCOCK,       SUN, t(11,30), t(12,45)),
    Act("Miss Sophie Lee",                                   HANCOCK,       SUN, t(13, 0), t(14,15)),
    Act("Mark Brooks",                                       HANCOCK,       SUN, t(14,30), t(15,45)),
    Act("New Orleans High Society",                          HANCOCK,       SUN, t(16, 0), t(17,15)),

    Act("Jason Mingledorff",                                 OMNI,          SUN, t(11,15), t(12,30)),
    Act("Father Ron and Friends",                            OMNI,          SUN, t(12,45), t(14, 0)),
    Act("Sweetie Pies of New Orleans",                       OMNI,          SUN, t(14,15), t(15,30)),
    Act("Ecirb Müller's Twisted Dixie",                      OMNI,          SUN, t(15,45), t(17, 0)),

    Act("Capivaras Jazz Quartet",                            KREWE,         SUN, t(11, 0), t(12,15)),
    Act("The New Orleans Jazz Vipers",                       KREWE,         SUN, t(12,30), t(13,45)),
    Act("Seva Venet's Traditional Line-Up",                  KREWE,         SUN, t(14, 0), t(15,15)),
    Act("Harry Mayronne & Chloe Marie",                      KREWE,         SUN, t(15,30), t(16,45)),

    Act("Steamboat Willy",                                   CAFEBEIGNET,   SUN, t(11,30), t(14, 0)),
    Act("Steve Rohbock Trio",                                CAFEBEIGNET,   SUN, t(14,30), t(17, 0)),
]


# ── Query API ──────────────────────────────────────────────────────────────────

def at(query_date: date, query_time: time) -> list[Act]:
    """Return all acts playing at a given date and time."""
    return sorted(
        [a for a in SCHEDULE if a.date == query_date and a.start <= query_time < a.end],
        key=lambda a: a.stage
    )


def search(query: str) -> list[Act]:
    """Case-insensitive substring search across act name and stage name."""
    q = query.lower()
    return sorted(
        [a for a in SCHEDULE if q in a.name.lower() or q in a.stage.lower()],
        key=lambda a: (a.date, a.start)
    )


def on(query_date: date, stage: Optional[str] = None) -> list[Act]:
    """Return all acts on a given date, optionally filtered by stage substring."""
    results = [a for a in SCHEDULE if a.date == query_date]
    if stage:
        results = [a for a in results if stage.lower() in a.stage.lower()]
    return sorted(results, key=lambda a: (a.stage, a.start))


def print_acts(acts: list[Act]) -> None:
    if not acts:
        print("  (no results)")
        return
    for a in acts:
        print(f"  {a}")


# ── CLI demo ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"\nTotal acts loaded: {len(SCHEDULE)}\n")

    print("=== at(FRI, 2:00 PM) ===")
    print_acts(at(FRI, t(14, 0)))

    print("\n=== search('brass band') ===")
    print_acts(search("brass band"))

    print("\n=== search('Stanton Moore') ===")
    print_acts(search("Stanton Moore"))

    print("\n=== search('Banu Gibson') ===")
    print_acts(search("Banu Gibson"))

    print("\n=== on(SAT, stage='Fish Fry') ===")
    print_acts(on(SAT, "Fish Fry"))
