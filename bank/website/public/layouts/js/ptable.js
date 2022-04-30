var canvas = document.getElementById('ptable-canvas');
var selection = document.getElementById('selection-canvas');
var ctx = canvas.getContext('2d');
var sel = selection.getContext('2d');

table = [
	[1,   3,  11,  19,  37,  55,  87,   0,   0],
	[0,   4,  12,  20,  38,  56,  88,   0,   0],
	[0,   0,   0,  21,  39, 119, 120,  57,  89],
	[0,   0,   0,  22,  40,  72, 104,  58,  90],
	[0,   0,   0,  23,  41,  73, 105,  59,  91],
	[0,   0,   0,  24,  42,  74, 106,  60,  92],
	[0,   0,   0,  25,  43,  75, 107,  61,  93],
	[0,   0,   0,  26,  44,  76, 108,  62,  94],
	[0,   0,   0,  27,  45,  77, 109,  63,  95],
	[0,   0,   0,  28,  46,  78, 110,  64,  96],
	[0,   0,   0,  29,  47,  79, 111,  65,  97],
	[0,   0,   0,  30,  48,  80, 112,  66,  98],
	[0,   5,  13,  31,  49,  81, 113,  67,  99],
	[0,   6,  14,  32,  50,  82, 114,  68, 100],
	[0,   7,  15,  33,  51,  83, 115,  69, 101],
	[0,   8,  16,  34,  52,  84, 116,  70, 102],
	[0,   9,  17,  35,  53,  85, 117,  71, 103],
	[2,  10,  18,  36,  54,  86, 118,   0,   0],
];

elements = [
	{},
	{abbreviation: 'H',  name: 'Hydrogen',  	type: 'nonmetal', 	  atomic_number:   '1', year: '1766', discoverer: 'Henry Cavendish'},
	{abbreviation: 'He', name: 'Helium', 		type: 'nonmetal', 	  atomic_number:   '2', year: '1868', discoverer: 'Pierre-Jules-César Janssen'},
	{abbreviation: 'Li', name: 'Lithium', 		type: 'metal', 		  atomic_number:   '3', year: '1817', discoverer: 'Johann August Arfvedson'},
	{abbreviation: 'Be', name: 'Beryllium', 	type: 'metal', 		  atomic_number:   '4', year: '1798', discoverer: 'Louis-Nicholas Vauquelin'},
	{abbreviation: 'B',  name: 'Boron', 		type: 'transitional', atomic_number:   '5', year: '1808', discoverer: 'Joseph-Louis Gay-Lussac, Louis-Jaques Thénard, and Sir Humphry Davy'},
	{abbreviation: 'C',  name: 'Carbon', 		type: 'nonmetal', 	  atomic_number:   '6', year: '----', discoverer: 'N/A'},
	{abbreviation: 'N',  name: 'Nitrogen', 		type: 'nonmetal', 	  atomic_number:   '7', year: '1772', discoverer: 'Daniel Rutherford'},
	{abbreviation: 'O',  name: 'Oxygen', 		type: 'nonmetal', 	  atomic_number:   '8', year: '1774', discoverer: 'Joseph Priestley'},
	{abbreviation: 'F',  name: 'Fluorine', 		type: 'nonmetal', 	  atomic_number:   '9', year: '1886', discoverer: 'Ferdinand Frederic Henri Moissan'},
	{abbreviation: 'Ne', name: 'Neon', 			type: 'nonmetal', 	  atomic_number:  '10', year: '1898', discoverer: '	Sir William Ramsay and Morris M. Travers'},
	{abbreviation: 'Na', name: 'Sodium', 		type: 'metal', 	  	  atomic_number:  '11', year: '1807', discoverer: 'Sir Humphry Davy'},
	{abbreviation: 'Mg', name: 'Magnesium', 	type: 'metal', 	  	  atomic_number:  '12', year: '1808', discoverer: 'Sir Humphry Davy'},
	{abbreviation: 'Al', name: 'Aluminum', 		type: 'metal', 	  	  atomic_number:  '13', year: '1825', discoverer: 'Hans Christian Oersted'},
	{abbreviation: 'Si', name: 'Silicon', 		type: 'transitional', atomic_number:  '14', year: '1824', discoverer: 'Jöns Jacob Berzelius'},
	{abbreviation: 'P',  name: 'Phosphorus', 	type: 'nonmetal', 	  atomic_number:  '15', year: '1669', discoverer: 'Hennig Brand'},
	{abbreviation: 'S',  name: 'Sulfur', 		type: 'nonmetal', 	  atomic_number:  '16', year: '----', discoverer: 'N/A'},
	{abbreviation: 'Cl', name: 'Chlorine', 		type: 'nonmetal', 	  atomic_number:  '17', year: '1774', discoverer: 'Carl Wilhelm Scheele'},
	{abbreviation: 'Ar', name: 'Argon', 		type: 'nonmetal', 	  atomic_number:  '18', year: '1894', discoverer: 'Sir William Ramsay and Lord Rayleigh'},
	{abbreviation: 'K',  name: 'Potassium', 	type: 'metal', 		  atomic_number:  '19', year: '1807', discoverer: 'Sir Humphry Davy'},
	{abbreviation: 'Ca', name: 'Calcium', 		type: 'metal', 		  atomic_number:  '20', year: '1808', discoverer: 'Sir Humphry Davy'},
	{abbreviation: 'Sc', name: 'Scandium', 		type: 'metal', 		  atomic_number:  '21', year: '1879', discoverer: 'Lars Fredrik Nilson'},
	{abbreviation: 'Ti', name: 'Titanium', 		type: 'metal', 		  atomic_number:  '22', year: '1791', discoverer: 'The Reverend William Gregor'},
	{abbreviation: 'V',  name: 'Vanadium', 		type: 'metal', 		  atomic_number:  '23', year: '1801 and 1830', discoverer: 'Andrés Manuel del Rio and separately by Nils Gabriel Sefstrôm, respectively'},
	{abbreviation: 'Cr', name: 'Chromium', 		type: 'metal', 		  atomic_number:  '24', year: '1797', discoverer: 'Louis-Nicholas Vauquelin'},
	{abbreviation: 'Mn', name: 'Manganese', 	type: 'metal', 		  atomic_number:  '25', year: '1774', discoverer: 'Johan Gottlieb Gahn'},
	{abbreviation: 'Fe', name: 'Iron',	 		type: 'metal', 		  atomic_number:  '26', year: '----', discoverer: 'N/A'},
	{abbreviation: 'Co', name: 'Cobalt', 		type: 'metal', 		  atomic_number:  '27', year: '1739', discoverer: 'Georg Brandt'},
	{abbreviation: 'Ni', name: 'Nickel', 		type: 'metal', 		  atomic_number:  '28', year: '1751', discoverer: 'Axel Fredrik Cronstedt'},
	{abbreviation: 'Cu', name: 'Copper', 		type: 'metal', 		  atomic_number:  '29', year: '----', discoverer: 'N/A'},
	{abbreviation: 'Zn', name: 'Zinc', 			type: 'metal', 		  atomic_number:  '30', year: '----', discoverer: 'N/A'},
	{abbreviation: 'Ga', name: 'Gallium', 		type: 'metal', 		  atomic_number:  '31', year: '1875', discoverer: 'Paul-Émile Lecoq de Boisbaudran'},
	{abbreviation: 'Ge', name: 'Germanium', 	type: 'transitional', atomic_number:  '32', year: '1886', discoverer: 'Clemens Winkler'},
	{abbreviation: 'As', name: 'Arsenic', 		type: 'transitional', atomic_number:  '33', year: '----', discoverer: 'N/A'},
	{abbreviation: 'Se', name: 'Selenium', 		type: 'nonmetal', 	  atomic_number:  '34', year: '1817', discoverer: 'Jöns Jacob Berzelius'},
	{abbreviation: 'Br', name: 'Bromine', 		type: 'nonmetal', 	  atomic_number:  '35', year: '1826', discoverer: 'Antoine-Jérôme Balard'},
	{abbreviation: 'Kr', name: 'Krypton', 		type: 'nonmetal', 	  atomic_number:  '36', year: '1898', discoverer: 'Sir William Ramsay and Morris M. Travers'},
	{abbreviation: 'Rb', name: 'Rubidium', 		type: 'metal', 	  	  atomic_number:  '37', year: '1861', discoverer: 'Robert Bunsen and Gustav Kirchhoff'},
	{abbreviation: 'Sr', name: 'Strontium', 	type: 'metal', 	  	  atomic_number:  '38', year: '1790', discoverer: 'Adair Crawford'},
	{abbreviation: 'Y',  name: 'Yttrium', 		type: 'metal', 	  	  atomic_number:  '39', year: '1789', discoverer: 'Johan Gadolin'},
	{abbreviation: 'Zr', name: 'Zirconium', 	type: 'metal', 	  	  atomic_number:  '40', year: '1789', discoverer: 'Martin Heinrich Klaproth'},
	{abbreviation: 'Nb', name: 'Niobium', 		type: 'metal', 	  	  atomic_number:  '41', year: '1801', discoverer: 'Charles Hatchett'},
	{abbreviation: 'Mo', name: 'Molybdenum', 	type: 'metal', 	  	  atomic_number:  '42', year: '1778', discoverer: 'Carl Welhelm Scheele'},
	{abbreviation: 'Tc', name: 'Technetium', 	type: 'metal', 	  	  atomic_number:  '43', year: '1937', discoverer: 'Carlo Perrier and Emilio Segrè'},
	{abbreviation: 'Ru', name: 'Ruthenium', 	type: 'metal', 	  	  atomic_number:  '44', year: '1844', discoverer: 'Karl Karlovich Klaus'},
	{abbreviation: 'Rh', name: 'Rhodium', 		type: 'metal', 	  	  atomic_number:  '45', year: '1803', discoverer: 'William Hyde Wollaston'},
	{abbreviation: 'Pd', name: 'Palladium', 	type: 'metal', 	  	  atomic_number:  '46', year: '1803', discoverer: 'William Hyde Wollaston'},
	{abbreviation: 'Ag', name: 'Silver', 		type: 'metal', 	  	  atomic_number:  '47', year: '----', discoverer: 'N/A'},
	{abbreviation: 'Cd', name: 'Cadmium', 		type: 'metal', 	  	  atomic_number:  '48', year: '1817', discoverer: 'Friedrich Strohmeyer'},
	{abbreviation: 'In', name: 'Indium', 		type: 'metal', 	  	  atomic_number:  '49', year: '1863', discoverer: 'Ferdinand Reich and Hieronymus Theodor Richter'},
	{abbreviation: 'Sn', name: 'Tin', 			type: 'metal', 	  	  atomic_number:  '50', year: '----', discoverer: 'N/A'},
	{abbreviation: 'Sb', name: 'Antimony', 		type: 'transitional', atomic_number:  '51', year: '----', discoverer: 'N/A'},
	{abbreviation: 'Te', name: 'Tellurium', 	type: 'transitional', atomic_number:  '52', year: '1782', discoverer: 'Franz Joseph Müller von Reichenstein'},
	{abbreviation: 'I',  name: 'Iodine', 		type: 'nonmetal', 	  atomic_number:  '53', year: '1811', discoverer: 'Barnard Courtois'},
	{abbreviation: 'Xe', name: 'Xenon', 		type: 'nonmetal', 	  atomic_number:  '54', year: '1898', discoverer: 'Sir William Ramsay and Morris M. Travers'},
	{abbreviation: 'Cs', name: 'Cesium', 		type: 'metal', 	  	  atomic_number:  '55', year: '1860', discoverer: 'Robert Wilhelm Bunsen and Gustav Robert Kirchoff'},
	{abbreviation: 'Ba', name: 'Barium', 		type: 'metal', 	  	  atomic_number:  '56', year: '1808', discoverer: 'Sir Humphry Davy	'},
	{abbreviation: 'La', name: 'Lanthanum', 	type: 'lanthanide',   atomic_number:  '57', year: '1839', discoverer: 'Carl Gustaf Mosander'},
	{abbreviation: 'Ce', name: 'Cerium', 		type: 'lanthanide',   atomic_number:  '58', year: '1803', discoverer: 'Jöns Jacob Berzelius, Wilhelm von Hisinger, and Martin Heinrich Klaproth'},
	{abbreviation: 'Pr', name: 'Praseodymium', 	type: 'lanthanide',   atomic_number:  '59', year: '1885', discoverer: 'Carl F. Auer von Welsbach'},
	{abbreviation: 'Nd', name: 'Neodymium', 	type: 'lanthanide',   atomic_number:  '60', year: '1885', discoverer: 'Carl F. Auer von Welsbach'},
	{abbreviation: 'Pm', name: 'Promethium', 	type: 'lanthanide',   atomic_number:  '61', year: '1944', discoverer: 'Jacob A. Marinsky, Lawrence E. Glendenin, and Charles D. Coryell'},
	{abbreviation: 'Sm', name: 'Samarium', 		type: 'lanthanide',   atomic_number:  '62', year: '1853', discoverer: 'Jean Charles Galissard de Marignac'},
	{abbreviation: 'Eu', name: 'Europium', 		type: 'lanthanide',   atomic_number:  '63', year: '1896', discoverer: 'Eugène-Antole Demarçay'},
	{abbreviation: 'Gd', name: 'Gadolinium', 	type: 'lanthanide',   atomic_number:  '64', year: '1880', discoverer: 'Jean Charles Galissard de Marignac'},
	{abbreviation: 'Tb', name: 'Terbium', 		type: 'lanthanide',   atomic_number:  '65', year: '1843', discoverer: 'Carl Gustaf Mosander'},
	{abbreviation: 'Dy', name: 'Dysprosium', 	type: 'lanthanide',   atomic_number:  '66', year: '1886', discoverer: 'Paul-Émile Lecoq de Boisbaudran'},
	{abbreviation: 'Ho', name: 'Holmium', 		type: 'lanthanide',   atomic_number:  '67', year: '1879', discoverer: 'Per Theodor Cleve'},
	{abbreviation: 'Er', name: 'Erbium', 		type: 'lanthanide',   atomic_number:  '68', year: '1843', discoverer: 'Carl Gustaf Mosander'},
	{abbreviation: 'Tm', name: 'Thulium', 		type: 'lanthanide',   atomic_number:  '69', year: '1879', discoverer: 'Per Theodor Cleve'},
	{abbreviation: 'Yb', name: 'Ytterbium', 	type: 'lanthanide',   atomic_number:  '70', year: '1878', discoverer: 'Jean Charles Galissard de Marignac'},
	{abbreviation: 'Lu', name: 'Lutetium', 		type: 'lanthanide',   atomic_number:  '71', year: '1907', discoverer: 'Georges Urbain'},
	{abbreviation: 'Hf', name: 'Hafnium', 		type: 'metal', 		  atomic_number:  '72', year: '1923', discoverer: 'Dirk Coster and Charles de Hevesy'},
	{abbreviation: 'Ta', name: 'Tantalum', 		type: 'metal', 		  atomic_number:  '73', year: '1802', discoverer: 'Anders Gustaf Ekenberg'},
	{abbreviation: 'W',  name: 'Tungsten', 		type: 'metal', 		  atomic_number:  '74', year: '1783', discoverer: 'Juan José and Fausto Elhuyar'},
	{abbreviation: 'Re', name: 'Rhenium', 		type: 'metal', 		  atomic_number:  '75', year: '1925', discoverer: 'Ida Tacke-Noddack, Walter Noddack, and Otto Carl Berg'},
	{abbreviation: 'Os', name: 'Osmium', 		type: 'metal', 		  atomic_number:  '76', year: '1803', discoverer: 'Smithson Tennant'},
	{abbreviation: 'Ir', name: 'Iridium', 		type: 'metal', 		  atomic_number:  '77', year: '1803', discoverer: 'Smithson Tennant'},
	{abbreviation: 'Pt', name: 'Platinum', 		type: 'metal', 		  atomic_number:  '78', year: '1735', discoverer: 'Antonio de Ulloa, but was also known to Indigenous peoples of America'},
	{abbreviation: 'Au', name: 'Gold', 			type: 'metal', 		  atomic_number:  '79', year: '----', discoverer: 'N/A'},
	{abbreviation: 'Hg', name: 'Mercury', 		type: 'metal', 		  atomic_number:  '80', year: '----', discoverer: 'N/A'},
	{abbreviation: 'Tl', name: 'Thallium', 		type: 'metal', 		  atomic_number:  '81', year: '1861', discoverer: 'Sir William Crookes'},
	{abbreviation: 'Pb', name: 'Lead', 			type: 'metal', 		  atomic_number:  '82', year: '----', discoverer: 'N/A'},
	{abbreviation: 'Bi', name: 'Bismuth', 		type: 'metal', 		  atomic_number:  '83', year: '1753', discoverer: 'Claude Geoffroy the Younger'},
	{abbreviation: 'Po', name: 'Polonium', 		type: 'metal', 		  atomic_number:  '84', year: '1898', discoverer: 'Marie Sklodowska Curie'},
	{abbreviation: 'At', name: 'Astatine', 		type: 'transitional', atomic_number:  '85', year: '1940', discoverer: 'Dale R. Carson, K.R. MacKenzie, and Emilio Segrè'},
	{abbreviation: 'Rn', name: 'Radon', 		type: 'nonmetal', 	  atomic_number:  '86', year: '1900', discoverer: 'Friedrich Ernst Dorn'},
	{abbreviation: 'Fr', name: 'Francium', 		type: 'metal',		  atomic_number:  '87', year: '1939', discoverer: 'Marguerite Catherine Perey'},
	{abbreviation: 'Ra', name: 'Radium', 		type: 'metal',		  atomic_number:  '88', year: '1898', discoverer: 'Marie Sklodowska Curie and Pierre Curie'},
	{abbreviation: 'Ac', name: 'Actinium', 		type: 'actinide', 	  atomic_number:  '89', year: '1899', discoverer: 'André-Louis Debierne'},
	{abbreviation: 'Th', name: 'Thorium', 		type: 'actinide', 	  atomic_number:  '90', year: '1828', discoverer: 'Jöns Jacob Berzelius'},
	{abbreviation: 'Pa', name: 'Protactinium', 	type: 'actinide', 	  atomic_number:  '91', year: '1913', discoverer: 'Kasimir Fajans and O.H. Göhring'},
	{abbreviation: 'U',  name: 'Uranium',		type: 'actinide', 	  atomic_number:  '92', year: '1789', discoverer: 'Martin Heinrich Klaproth'},
	{abbreviation: 'Np', name: 'Neptunium', 	type: 'actinide', 	  atomic_number:  '93', year: '1940', discoverer: 'Edwin M. McMillian and Philip H. Abelson'},
	{abbreviation: 'Pu', name: 'Plutonium', 	type: 'actinide', 	  atomic_number:  '94', year: '1941', discoverer: 'Glenn T. Seaborg, Joseph W. Kennedy, Edward M. McMillan, and Arthur C. Wohl'},
	{abbreviation: 'Am', name: 'Americium', 	type: 'actinide', 	  atomic_number:  '95', year: '1944', discoverer: 'Glenn T. Seaborg, Ralph A. James, Leon O. Morgan, and Albert Ghiorso'},
	{abbreviation: 'Cm', name: 'Curium', 		type: 'actinide', 	  atomic_number:  '96', year: '1944', discoverer: 'Glenn T. Seaborg, Ralph A. James, and Albert Ghiorso'},
	{abbreviation: 'Bk', name: 'Berkelium', 	type: 'actinide', 	  atomic_number:  '97', year: '1949', discoverer: 'Stanley G. Thompson, Glenn T. Seaborg, Kenneth Street, Jr., and Albert Ghiorso'},
	{abbreviation: 'Cf', name: 'Californium', 	type: 'actinide', 	  atomic_number:  '98', year: '1950', discoverer: 'Stanley G. Thompson, Glenn T. Seaborg, Kenneth Street, Jr., and Albert Ghiorso'},
	{abbreviation: 'Es', name: 'Einsteinium', 	type: 'actinide', 	  atomic_number:  '99', year: '1952', discoverer: 'Albert Ghiorso et. al'},
	{abbreviation: 'Fm', name: 'Fermium', 		type: 'actinide', 	  atomic_number: '100', year: '1952', discoverer: 'Albert Ghiorso et. al'},
	{abbreviation: 'Md', name: 'Mendelevium', 	type: 'actinide', 	  atomic_number: '101', year: '1955', discoverer: 'Stanley G. Thompson, Glenn T. Seaborg, Bernard G. Harvey, Gregory R. Choppin, and Albert Ghiorso'},
	{abbreviation: 'No', name: 'Nobelium', 		type: 'actinide', 	  atomic_number: '102', year: '1958', discoverer: 'Albert Ghiorso, Glenn T. Seaborg, Torbørn Sikkeland, and John R. Walton'},
	{abbreviation: 'Lr', name: 'Lawrencium', 	type: 'actinide', 	  atomic_number: '103', year: '1961', discoverer: 'Albert Ghiorso, Torbjørn Sikkeland, Almon E. Larsh, and Robert M. Latimer'},
	{abbreviation: 'Rf', name: 'Rutherfordium', type: 'metal', 	      atomic_number: '104', year: '1964 and 1969', discoverer: 'Scientists in Dubna, Russia and separately by Albert Ghiorso et. al., respectively'},
	{abbreviation: 'Db', name: 'Dubnium', 		type: 'metal', 	      atomic_number: '105', year: '1967 and 1970', discoverer: 'scientists in Dubna, Russia and separately by scientists in Lawrence Berkeley Laboratory, respectively'},
	{abbreviation: 'Sg', name: 'Seaborgium', 	type: 'metal', 	      atomic_number: '106', year: '1974', discoverer: 'Albert Ghiorso et. al'},
	{abbreviation: 'Bh', name: 'Bohrium', 		type: 'metal', 	      atomic_number: '107', year: '1976', discoverer: 'scientists in Dubna, Russia'},
	{abbreviation: 'Hs', name: 'Hassium', 		type: 'metal', 	      atomic_number: '108', year: '1984', discoverer: 'Peter Armbruster and Gottfried Münzenber'},
	{abbreviation: 'Mt', name: 'Meitnerium', 	type: 'metal', 	      atomic_number: '109', year: '1982', discoverer: 'Peter Armbruster and Gottfried Münzenber'},
	{abbreviation: 'Ds', name: 'Darmstadtium', 	type: 'metal', 	      atomic_number: '110', year: '1994', discoverer: 'Peter Armbruster and Gottfried Münzenber'},
	{abbreviation: 'Rg', name: 'Roentgenium', 	type: 'metal', 	      atomic_number: '111', year: '1994', discoverer: 'Peter Armbruster and Gottfried Münzenber'},
	{abbreviation: 'Cn', name: 'Copernicium', 	type: 'metal', 	      atomic_number: '112', year: '1996', discoverer: 'Peter Armbruster and Gottfried Münzenber'},
	{abbreviation: 'Nh', name: 'Nihonium', 		type: 'metal', 	      atomic_number: '113', year: '2003', discoverer: 'Kosuke Morita et. al'},
	{abbreviation: 'Fl', name: 'Flerovium', 	type: 'metal', 	      atomic_number: '114', year: '1998', discoverer: 'scientists in Dubna, Russia with scientists from Lawrence Livermore National Laboratory'},
	{abbreviation: 'Mc', name: 'Moscovium', 	type: 'metal', 	      atomic_number: '115', year: '2003', discoverer: 'scientists in Dubna, Russia, Lawrence Livermore National Laboratory in California, USA, and Oak Ridge National Laboratory in Tennessee, USA'},
	{abbreviation: 'Lv', name: 'Livermorium', 	type: 'metal', 	      atomic_number: '116', year: '2001', discoverer: 'scientists in Dubna, Russia with scientists from Lawrence Livermore National Laboratory'},
	{abbreviation: 'Ts', name: 'Tennessine', 	type: 'metal', 	      atomic_number: '117', year: '2010', discoverer: 'Yuri Tsolakovich Oganessian et. al'},
	{abbreviation: 'Og', name: 'Oganesson', 	type: 'nonmetal', 	  atomic_number: '118', year: '2002', discoverer: 'Yuri Tsolakovich Oganessian et. al'},
	{abbreviation: '', 	 name: 'lanthanides', 	type: 'lanthanide',   atomic_number: 	'', year: '', discoverer: ''},
	{abbreviation: '',   name: 'actinides', 	type: 'actinide', 	  atomic_number: 	'', year: '', discoverer: ''}
];

colors = {
	nonmetal: 'rgb(255, 128, 128)',
	metal: 'rgb(156, 218, 164)',
	transitional: 'rgb(128, 128, 255)',
	lanthanide: 'rgb(253, 215, 157)',
	actinide: 'rgb(253, 215, 157)'
}

var width = canvas.width;
var height = canvas.height;
var size = 0;
if (width < height) {
	size = height / 10;
} else {
	size = width / 19;
}
let squareSize = size;

function drawTable() {
	for (let i = 0; i < table.length; i++) {
		for (let j = 0; j < table[i].length; j++) {
			if (table[i][j] != 0) {
				element = elements[table[i][j]];
				makeElementSquare(element, table[i][j],
					{x: (i + 0.5) * squareSize, y: (j + 0.5) * squareSize},
					colors[element.type]);
			}
		}
	}
}

function makeElementSquare(element, id, loc, fillStyle) {
	// draw the square
	ctx.fillStyle = fillStyle;
	ctx.strokeStyle = 'rgb(255, 255, 255)';
	ctx.lineWidth = 2;
	ctx.fillRect(loc.x, loc.y, squareSize, squareSize);
	ctx.strokeRect(loc.x, loc.y, squareSize, squareSize);

	var fontSize;

	// check if label group
	if (element.name === 'Lanthanides' || element.name === 'Actinides') {
		fontSize = 15;
		ctx.textAlign = 'center';
		ctx.textBaseline = 'middle';
		ctx.font = `bold ${fontSize}px Nunito`;
		ctx.fillStyle = 'rgb(0, 0, 0)';
		ctx.fillText(element.name,
			loc.x + squareSize / 2, loc.y + squareSize / 2);
	} else {
		fontSize = 20;
		// draw the atomic number
		ctx.textAlign = 'start';
		ctx.textBaseline = 'top';
		ctx.fillStyle = 'rgb(0, 0, 0)';
		ctx.font = 'bold 10px Nunito';
		ctx.fillText(id, loc.x + squareSize * 0.05, loc.y + squareSize * 0.05);

		// draw the name
		ctx.textBaseline = 'alphabetic';
		ctx.font = 'bold 20px Nunito';
		while (ctx.measureText(element.name).width >= squareSize * 0.9) {
			fontSize--;
			ctx.font = `bold ${fontSize}px Nunito`;
		}
		var textSize = ctx.measureText(element.name);
		var textWidth = textSize.width;
		ctx.fillText(element.name,
			loc.x - (textWidth - squareSize) / 2,
			loc.y + squareSize * 0.9);

		// draw the abbreviation
		fontSize = 30;
		ctx.font = `bold ${fontSize}px Nunito`;
		ctx.textAlign = 'center';
		ctx.textBaseline = 'middle';
		ctx.fillText(element.abbreviation,
			loc.x + squareSize / 2, loc.y + squareSize / 2);
	}
}

function repaint() {
	ctx.fillStyle = 'rgb(255, 255, 255)';
	ctx.fillRect(0, 0, width, height);
	drawTable();
}

var selectedElement = null;
function selectElement(selectionPos) {
	let x = selectionPos.x;
	let y = selectionPos.y;
	offset = {w: squareSize/2, h: squareSize/2};
	var i = Math.floor((x - offset.w) / squareSize);
	var j = Math.floor((y - offset.h) / squareSize);
	sel.clearRect(0, 0, width, height);
	sel.strokeStyle = 'rgb(0, 0, 0)';
	sel.lineWidth = 2;
	// first check if the mouse is in bounds
	if (i >= 0 && i < 18 && j >= 0 && j < 9) {
		// next check if the mouse is highlighting an element
		var id = getSelectedElementID(i, j);
		if (id != 0) {
			sel.strokeRect(i * squareSize + offset.w, j * squareSize + offset.h,
				squareSize, squareSize);
			selectedElement = elements[id];
			paintSelectedElement();
			return true;
		} else {
			paintStandardElement();
			return false;
		}
	} else {
		paintStandardElement();
		return false;
	}
}

function getSelectedElementID(i, j) {
	if (i >= 0 && i < 18 && j >= 0 && j < 9) {
		return table[i][j];
	}
}

function clearSelection() {
	sel.clearRect(0, 0, width, height);
}

bel = {x: 6.5, y: 1.25};
function paintSelectedElement() {
	if (selectedElement != null) {
		// paint outline
		sel.fillStyle = colors[selectedElement.type];
		sel.fillRect((bel.x - 0.25) * squareSize, (bel.y - 0.25) * squareSize,
			2.5 * squareSize, 1.75 * squareSize);

		// paint element
		sel.fillStyle = 'rgb(0, 0, 0)';
		sel.font = 'bold 36px Nunito';
		sel.textAlign = 'center';
		sel.textBaseline = 'middle';
		sel.fillText(selectedElement.name, (bel.x + 1) * squareSize, (bel.y + 1) * squareSize);

		// paint atomic number
		sel.textAlign = 'start';
		sel.textBaseline = 'top';
		sel.fillText(selectedElement.atomic_number, bel.x * squareSize, bel.y * squareSize);

		// paint abbreviation
		sel.textAlign = 'end'
		sel.fillText(selectedElement.abbreviation, (bel.x + 2) * squareSize, bel.y * squareSize);

		// paint discovery information
		sel.font = 'bold 16px Nunito';
		sel.textAlign = 'start'
		var discoveryText;
		if (selectedElement.year != '----') {
			discoveryText = `${selectedElement.name} was discovered in ${selectedElement.year} by ${selectedElement.discoverer}.`;
		} else {
			discoveryText = `${selectedElement.name} has been known since ancient times.`
		}
		let lines = getLines(sel, discoveryText, 8 * squareSize);
		for (let i = 0; i < lines.length; i++) {
			let line = lines[i];
			sel.fillText(line, 3.5 * squareSize, i * 20 + 3 * squareSize);
		}
	}
}

function getLines(ctx, text, maxWidth) {
    var words = text.split(' ');
    var lines = [];
    var currentLine = words[0];

    for (var i = 1; i < words.length; i++) {
        var word = words[i];
        var width = ctx.measureText(currentLine + ' ' + word).width;
        if (width < maxWidth) {
            currentLine += ' ' + word;
        } else {
            lines.push(currentLine);
            currentLine = word;
        }
    }
    lines.push(currentLine);
    return lines;
}

function paintStandardElement() {
	// paint outline
	sel.fillStyle = 'rgb(215, 215, 215)';
	sel.fillRect((bel.x - 0.25) * squareSize, (bel.y - 0.25) * squareSize,
		2.5 * squareSize, 1.75 * squareSize);
	sel.fillStyle = 'rgb(0, 0, 0)';

	// paint element header
	sel.font = 'bold 36px Nunito';
	sel.textAlign = 'center';
	sel.textBaseline = 'middle';
	sel.fillText('Element', (bel.x + 1) * squareSize, (bel.y + 1) * squareSize);

	// paint atomic number
	sel.textAlign = 'start';
	sel.textBaseline = 'top';
	sel.fillText('0', bel.x * squareSize, bel.y * squareSize);

	// paint abbreviation
	sel.textAlign = 'end'
	sel.fillText('E', (bel.x + 2) * squareSize, bel.y * squareSize);
}

var boundingClientRect = canvas.getBoundingClientRect();
var scaleX = canvas.width / boundingClientRect.width;
var scaleY = canvas.height / boundingClientRect.height;
var selectionPos = {};
var moving = true;
document.addEventListener('mousemove', (e) => {
	selectionPos.x = (e.clientX - boundingClientRect.left) * scaleX;
	selectionPos.y = (e.clientY - boundingClientRect.top) * scaleY;
	if (moving) {
		selectElement(selectionPos);
	}
});

document.addEventListener('mousedown', (e) => {
	if (e.button === 0) { // left click
		if (selectElement(selectionPos)) {
			moving = false;
		}
	}
});

document.addEventListener('keydown', (e) => {
	switch (e.code) {
		case 'Escape':
			clearSelection();
			moving = true;
			break;
	}
});

// start the code
repaint();
