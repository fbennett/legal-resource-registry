var fs = require('fs')
var path = require('path')

var courtTemplate = ".. court:: --COURT_NAME--\n   :court-id: --JURISDICTION_ID--;--COURT_ID--\n"

var categoryTemplate = ".. category:: --JURISDICTION_NAME--\n   :category-id: --JURISDICTION_ID--\n"


var highCourts = [
    "auckland",
    "blenheim",
    "christchurch",
    "dunedin",
    "gisborne",
    "greymouth",
    "hamilton",
    "invercargill",
    "masterton",
    "napier",
    "nelson",
    "new.plymouth",
    "palmerston.north",
    "rotorua",
    "tauranga",
    "timaru",
    "wellington",
    "whanganui",
    "whangarei"
]

var maoriLandCourts = [
    "christchurch",
    "ellerslie",
    "gisborne",
    "hamilton",
    "rotorua",
    "whanganui",
    "wellington",
    "whangarei",
    "hastings"
]

var nationalCourts = {
    "supreme.court": {
        "name": "Supreme Court",
        "jurisdiction": "nz"
    },
    "court.appeal": {
        "name": "Court of Appeal",
        "jurisdiction": "nz"
    },
    "accident.compensation.appeal.authority": {
        "name": "Accident Compensation Appeal Authority",
        "jurisdiction": "nz"
    },
    "broadcasting.standards.authority": {
        "name": "Broadcasting Standards Authority",
        "jurisdiction": "nz"
    },
    "commerce.commission": {
        "name": "Commerce Commission",
        "jurisdiction": "nz"
    },
    "copyright.tribunal": {
        "name": "Copyright Tribunal",
        "jurisdiction": "nz"
    },
    "customs.appeal.authority": {
        "name": "Customs Appeal Authority",
        "jurisdiction": "nz"
    },
    "deportation.review.tribunal": {
        "name": "Deportation Review Tribunal",
        "jurisdiction": "nz"
    },
    "disputes.tribunal": {
        "name": "Disputes Tribunal",
        "jurisdiction": "nz"
    },
    "employment.relations.authority": {
        "name": "Employment Relations Authority",
        "jurisdiction": "nz"
    },
    "human.rights.review.tribunal": {
        "name": "Human Rights Review Tribunal",
        "jurisdiction": "nz"
    },
    "immigration.advisers.complaints.disciplinary.tribunal": {
        "name": "Immigration Advisers Complaints Disciplinary Tribunal",
        "jurisdiction": "nz"
    },
    "immigration.and.protection.tribunal": {
        "name": "Immigration and Protection Tribunal",
        "jurisdiction": "nz"
    },
    "international.education.appeal.authority": {
        "name": "International Education Appeal Authority",
        "jurisdiction": "nz"
    },
    "land.valuation.tribunal": {
        "name": "Land Valuation Tribunal",
        "jurisdiction": "nz"
    },
    "lawyers.and.conveyancers.disciplinary.tribunal": {
        "name": "Lawyers and Conveyancers Disciplinary Tribunal",
        "jurisdiction": "nz"
    },
    "legal.aid.tribunal": {
        "name": "Legal Aid Tribunal",
        "jurisdiction": "nz"
    },
    "licensing.authority.of.secondhand.dealers.and.pawnbrokers": {
        "name": "Licensing Authority of Secondhand Dealers and Pawnbrokers",
        "jurisdiction": "nz"
    },
    "liquor.licensing.authority": {
        "name": "Liquor Licensing Authority",
        "jurisdiction": "nz"
    },
    "mental.health.review.tribunal": {
        "name": "Mental Health Review Tribunal",
        "jurisdiction": "nz"
    },
    "motor.vehicle.disputes.tribunal": {
        "name": "Motor Vehicle Disputes Tribunal",
        "jurisdiction": "nz"
    },
    "private.security.personnel.licensing.authority": {
        "name": "Private Security Personnel Licensing Authority",
        "jurisdiction": "nz"
    },
    "real.estate.agents.disciplinary.tribunal": {
        "name": "Real Estate Agents Disciplinary Tribunal",
        "jurisdiction": "nz"
    },
    "social.security.appeal.authority": {
        "name": "Social Security Appeal Authority",
        "jurisdiction": "nz"
    },
    "taxation.review.authority": {
        "name": "Taxation Review Authority",
        "jurisdiction": "nz"
    },
    "tenancy.tribunal": {
        "name": "Tenancy Tribunal",
        "jurisdiction": "nz"
    },
    "weathertight.homes.tribunal": {
        "name": "Weathertight Homes Tribunal",
        "jurisdiction": "nz"
    }
}

function idToName(id) {
    var name = id.replace(/\./g, " ")
    var lst = name.split(/\s+/)
    for (var i=0,ilen=lst.length;i<ilen;i++) {
        var word = lst[i];
        lst[i] = word.slice(0, 1).toUpperCase() + word.slice(1);
    }
    name = lst.join(" ");
    return name;
}

function makeNationalCourts() {
    for (var courtID in nationalCourts) {
        
        var courtName = idToName(courtID)
        if (!fs.existsSync(courtID)) {
            fs.mkdirSync(courtID)
        }
        var newText = courtTemplate
	        .replace("--COURT_NAME--", courtName)
	        .replace("--JURISDICTION_ID--", "nz")
            .replace("--COURT_ID--", courtID)
        fs.writeFileSync(path.join(courtID, "index.txt"), newText)
        console.log(newText)
        
    }
}
makeNationalCourts()

function makeHighCourts() {
    for (var jurisdictionID of highCourts) {
        var jurisdictionName = idToName(jurisdictionID);
        if (!fs.existsSync(jurisdictionID)) {
            fs.mkdirSync(jurisdictionID)
        }
	    var newText = categoryTemplate
	        .replace("--JURISDICTION_NAME--", jurisdictionName)
            .replace("--JURISDICTION_ID--", "nz:" + jurisdictionID)
        fs.writeFileSync(path.join(jurisdictionID, "index.txt"), newText)
        console.log(newText)
        var courtDirPath = path.join(jurisdictionID, "high.court")
        if (!fs.existsSync(courtDirPath)) {
            fs.mkdirSync(courtDirPath)
        }
        var newText = courtTemplate
            .replace("--COURT_NAME--", "High Court")
            .replace("--JURISDICTION_ID--", "nz:" + jurisdictionID)
            .replace("--COURT_ID--", "high.court")
        fs.writeFileSync(path.join(courtDirPath, "index.txt"), newText)
        console.log(newText)
  }
}
makeHighCourts()

// NEED MAORI STUB
function makeMaoriLandCourts() {
    if (!fs.existsSync("maori")) {
        fs.mkdirSync("maori")
    }
	var newText = categoryTemplate
	    .replace("--JURISDICTION_NAME--", "Maori Land Court Jurisdiction")
        .replace("--JURISDICTION_ID--", "nz:maori")
    fs.writeFileSync(path.join("maori", "index.txt"), newText)
    console.log(newText)
    for (var jurisdictionID of maoriLandCourts) {
        var jurisdictionName = idToName(jurisdictionID);
        var maoriSubJurisdictionPath = path.join("maori", jurisdictionID);
        if (!fs.existsSync(maoriSubJurisdictionPath)) {
            fs.mkdirSync(maoriSubJurisdictionPath)
        }
	    var newText = categoryTemplate
	        .replace("--JURISDICTION_NAME--", jurisdictionName)
            .replace("--JURISDICTION_ID--", "nz:maori:" + jurisdictionID)
        fs.writeFileSync(path.join(maoriSubJurisdictionPath, "index.txt"), newText)
        console.log(newText)
        var maoriSubCourtPath = path.join(maoriSubJurisdictionPath, "land.court")
        if (!fs.existsSync(maoriSubCourtPath)) {
            fs.mkdirSync(maoriSubCourtPath)
        }
        var newText = courtTemplate
            .replace("--COURT_NAME--", "Land Court")
            .replace("--JURISDICTION_ID--", "nz:maori:" + jurisdictionID)
            .replace("--COURT_ID--", "land.court")
        fs.writeFileSync(path.join(maoriSubCourtPath, "index.txt"), newText)
        console.log(newText)
    }
}
makeMaoriLandCourts()
