__title__ = "perspective.py"
__author__ = "Yilmaz4"
__license__ = "MIT"
__copyright__ = "Copyright © 2017-2023 Yilmaz Alpaslan"
__version__ = "1.0.0"

all_attrs = ["TOXICITY", "SEVERE_TOXICITY", "IDENTITY_ATTACK", 
"INSULT", "PROFANITY", "THREAT", "TOXICITY_EXPERIMENTAL", 
"SEVERE_TOXICITY_EXPERIMENTAL", "IDENTITY_ATTACK_EXPERIMENTAL", 
"INSULT_EXPERIMENTAL", "PROFANITY_EXPERIMENTAL", 
"THREAT_EXPERIMENTAL", "SEXUALLY_EXPLICIT", "FLIRTATION",
"ATTACK_ON_AUTHOR", "ATTACK_ON_COMMENTER", "INCOHERENT", 
"INFLAMMATORY", "LIKELY_TO_REJECT", "OBSCENE", "SPAM", 
"UNSUBSTANTIAL"]

all_prod_attrs = ["TOXICITY", "SEVERE_TOXICITY", "IDENTITY_ATTACK", "INSULT", "PROFANITY", "THREAT"]
all_expr_attrs = ["TOXICITY_EXPERIMENTAL", "SEVERE_TOXICITY_EXPERIMENTAL", "IDENTITY_ATTACK_EXPERIMENTAL", "INSULT_EXPERIMENTAL", "PROFANITY_EXPERIMENTAL", "THREAT_EXPERIMENTAL", "SEXUALLY_EXPLICIT", "FLIRTATION"]
all_newy_attrs = ["ATTACK_ON_AUTHOR", "ATTACK_ON_COMMENTER", "INCOHERENT", "INFLAMMATORY", "LIKELY_TO_REJECT", "OBSCENE", "SPAM", "UNSUBSTANTIAL"]
class Attributes:
    class All:
        """
        ## All Attributes
        Every single attribute that Perspective API supports, such as Toxicity, Insult or Attack_on_author. As most of them are experimental, only common supported language among them is expected to be English (en).

        ### Common supported language(s)

        English (en)
        """
        supportedLanguages = ["en"]
        def __repr__(self):
            return """TOXICITY","SEVERE_TOXICITY","IDENTITY_ATTACK","INSULT","PROFANITY","THREAT","TOXICITY_EXPERIMENTAL","SEVERE_TOXICITY_EXPERIMENTAL","IDENTITY_ATTACK_EXPERIMENTAL","INSULT_EXPERIMENTAL","PROFANITY_EXPERIMENTAL","THREAT_EXPERIMENTAL","SEXUALLY_EXPLICIT","FLIRTATION","ATTACK_ON_AUTHOR","ATTACK_ON_COMMENTER","INCOHERENT","INFLAMMATORY","LIKELY_TO_REJECT","OBSCENE","SPAM","UNSUBSTANTIAL"""
    All = All()
    class Production:
        """
        ## All Attributes
        Production attributes (prod.) have been tested across multiple domains and trained on significant amounts of human-annotated comments. We recommend using production attributes for your API requests.

        ### Common supported language(s)

        German (de), English (en), Italian (it), Portuguese (pt), Russian (ru)
        """
        supportedLanguages = ["en"]
        def __repr__(self):
            return """TOXICITY","SEVERE_TOXICITY","IDENTITY_ATTACK","INSULT","PROFANITY","THREAT"""
    Production = Production()
    class Experimental:
        """
        ## All Attributes
        Experimental attributes (exp.) have not been tested as thoroughly as production attributes. We recommend using experimental attributes only in non-production environments where a human is identifying and correcting errors.

        ### Common supported language(s)

        English (en)

        ### Important notes on using experimental attributes:

         - Once experimental attributes are deprecated and production attributes are created, the experimental attribute will stop working. When that happens, you will need to update the API call's attribute name to the new production attribute name.
        
         - Expect language availability to change over time as we test attribute performance and move attributes to production.
        """
        supportedLanguages = ["en"]
        def __repr__(self):
            return """TOXICITY_EXPERIMENTAL","SEVERE_TOXICITY_EXPERIMENTAL","IDENTITY_ATTACK_EXPERIMENTAL","INSULT_EXPERIMENTAL","PROFANITY_EXPERIMENTAL","THREAT_EXPERIMENTAL","SEXUALLY_EXPLICIT","FLIRTATION"""
    Experimental = Experimental()
    class NewYorkTimes:
        """
        ## All Attributes
        These attributes are experimental because they are trained on a single source of comments—New York Times (NYT) data tagged by their moderation team—and therefore may not work well for every use case.

        ### Common supported language(s)

        English (en)
        """
        supportedLanguages = ["en"]
        def __repr__(self):
            return """ATTACK_ON_AUTHOR","ATTACK_ON_COMMENTER","INCOHERENT","INFLAMMATORY","LIKELY_TO_REJECT","OBSCENE","SPAM","UNSUBSTANTIAL"""
    NewYorkTimes = NewYorkTimes()

    # Production attributes
    class TOXICITY:
        """
        ## TOXICITY
        A rude, disrespectful, or unreasonable comment that is likely to make people leave a discussion.

        ### Supported language(s)

        Arabic (ar), Chinese (zh), Czech (cs), Dutch (nl), English (en), French (fr), German (de),
        Hindi (hi), Hinglish (hi-Latn), Indonesian (id), Italian (it), Japanese (ja), Korean (ko),
        Polish (pl), Portuguese (pt), Russian (ru), Spanish (es)
        """
        supportedLanguages = ["ar", "zh", "cs", "nl", "en", "fr", "de", "hi", "id", "it", "ja", "ko", "pl", "pt", "ru", "es"]
        description = "A rude, disrespectful, or unreasonable comment that is likely to make people leave a discussion."
        isExperimental = False
        def __repr__(self):
            return "TOXICITY"
    TOXICITY = TOXICITY()
    class SEVERE_TOXICITY:
        """
        ## SEVERE_TOXICITY
        A very hateful, aggressive, disrespectful comment or otherwise very likely to make a user leave
        a discussion or give up on sharing their perspective. This attribute is much less sensitive to
        more mild forms of toxicity, such as comments that include positive uses of curse words.

        ### Supported language(s)

        German (de), English (en), Spanish (es), French (fr), Italian (it), Portuguese (pt), Russian (ru)
        """
        supportedLanguages = ["de", "en", "es", "fr", "it", "pt", "ru"]
        description = "A very hateful, aggressive, disrespectful comment or otherwise very likely to make a user leave a discussion or give up on sharing their perspective. This attribute is much less sensitive to more mild forms of toxicity, such as comments that include positive uses of curse words."
        isExperimental = False
        def __repr__(self):
            return "SEVERE_TOXICITY"
    SEVERE_TOXICITY = SEVERE_TOXICITY()
    class IDENTITY_ATTACK:
        """
        ## IDENTITY_ATTACK
        Negative or hateful comments targeting someone because of their identity.

        ### Supported language(s)

        German (de), English (en), Italian (it), Portuguese (pt), Russian (ru)
        """
        supportedLanguages = ["de", "en", "it", "pt", "ru"]
        description = "Negative or hateful comments targeting someone because of their identity."
        isExperimental = False
        def __repr__(self):
            return "IDENTITY_ATTACK"
    IDENTITY_ATTACK = IDENTITY_ATTACK()
    class INSULT:
        """
        ## INSULT
        Insulting, inflammatory, or negative comment towards a person or a group of people.

        ### Supported language(s)

        German (de), English (en), Italian (it), Portuguese (pt), Russian (ru)
        """
        supportedLanguages = ["de", "en", "it", "pt", "ru"]
        description = "Insulting, inflammatory, or negative comment towards a person or a group of people."
        isExperimental = False
        def __repr__(self):
            return "INSULT"
    INSULT = INSULT()
    class PROFANITY:
        """
        ## PROFANITY
        Swear words, curse words, or other obscene or profane language.

        ### Supported language(s)

        German (de), English (en), Italian (it), Portuguese (pt), Russian (ru)
        """
        supportedLanguages = ["de", "en", "it", "pt", "ru"]
        description = "Swear words, curse words, or other obscene or profane language."
        isExperimental = False
        def __repr__(self):
            return "PROFANITY"
    PROFANITY = PROFANITY()
    class THREAT:
        """
        ## THREAT
        Describes an intention to inflict pain, injury, or violence against an individual or group.

        ### Supported language(s)

        German (de), English (en), Italian (it), Portuguese (pt), Russian (ru)
        """
        supportedLanguages = ["de", "en", "it", "pt", "ru"]
        description = "Describes an intention to inflict pain, injury, or violence against an individual or group."
        isExperimental = False
        def __repr__(self):
            return "THREAT"
    THREAT = THREAT()

    # Experimental attributes
    class TOXICITY_EXPERIMENTAL:
        """
        ## TOXICITY_EXPERIMENTAL
        A rude, disrespectful, or unreasonable comment that is likely to make people leave a discussion.

        ### Important notes on using experimental attributes:

         - Once experimental attributes are deprecated and production attributes are created, the experimental attribute will stop working. When that happens, you will need to update the API call's attribute name to the new production attribute name.
        
         - Expect language availability to change over time as we test attribute performance and move attributes to production.

        """
        description = "A rude, disrespectful, or unreasonable comment that is likely to make people leave a discussion."
        isExperimental = True
        def __repr__(self):
            return "TOXICITY_EXPERIMENTAL"
    TOXICITY_EXPERIMENTAL = TOXICITY_EXPERIMENTAL()
    class SEVERE_TOXICITY_EXPERIMENTAL:
        """
        ## SEVERE_TOXICITY_EXPERIMENTAL
        A very hateful, aggressive, disrespectful comment or otherwise very likely to make a user leave
        a discussion or give up on sharing their perspective. This attribute is much less sensitive to
        more mild forms of toxicity, such as comments that include positive uses of curse words.

        ### Important notes on using experimental attributes:

         - Once experimental attributes are deprecated and production attributes are created, the experimental attribute will stop working. When that happens, you will need to update the API call's attribute name to the new production attribute name.
        
         - Expect language availability to change over time as we test attribute performance and move attributes to production.

        """
        description = "A very hateful, aggressive, disrespectful comment or otherwise very likely to make a user leave a discussion or give up on sharing their perspective. This attribute is much less sensitive to more mild forms of toxicity, such as comments that include positive uses of curse words."
        isExperimental = True
        def __repr__(self):
            return "SEVERE_TOXICITY_EXPERIMENTAL"
    SEVERE_TOXICITY_EXPERIMENTAL = SEVERE_TOXICITY_EXPERIMENTAL()
    class IDENTITY_ATTACK_EXPERIMENTAL:
        """
        ## IDENTITY_ATTACK_EXPERIMENTAL
        Negative or hateful comments targeting someone because of their identity.

        ### Important notes on using experimental attributes:

         - Once experimental attributes are deprecated and production attributes are created, the experimental attribute will stop working. When that happens, you will need to update the API call's attribute name to the new production attribute name.
        
         - Expect language availability to change over time as we test attribute performance and move attributes to production.

        """
        description = "Negative or hateful comments targeting someone because of their identity."
        isExperimental = True
        def __repr__(self):
            return "IDENTITY_ATTACK_EXPERIMENTAL"
    IDENTITY_ATTACK_EXPERIMENTAL = IDENTITY_ATTACK_EXPERIMENTAL()
    class INSULT_EXPERIMENTAL:
        """
        ## INSULT_EXPERIMENTAL
        Insulting, inflammatory, or negative comment towards a person or a group of people.

        ### Important notes on using experimental attributes:

         - Once experimental attributes are deprecated and production attributes are created, the experimental attribute will stop working. When that happens, you will need to update the API call's attribute name to the new production attribute name.
        
         - Expect language availability to change over time as we test attribute performance and move attributes to production.

        """
        description = "Insulting, inflammatory, or negative comment towards a person or a group of people."
        isExperimental = True
        def __repr__(self):
            return "INSULT_EXPERIMENTAL"
    INSULT_EXPERIMENTAL = INSULT_EXPERIMENTAL()
    class PROFANITY_EXPERIMENTAL:
        """
        ## PROFANITY_EXPERIMENTAL
        Swear words, curse words, or other obscene or profane language.

        ### Important notes on using experimental attributes:

         - Once experimental attributes are deprecated and production attributes are created, the experimental attribute will stop working. When that happens, you will need to update the API call's attribute name to the new production attribute name.
        
         - Expect language availability to change over time as we test attribute performance and move attributes to production.

        """
        description = "Swear words, curse words, or other obscene or profane language."
        isExperimental = True
        def __repr__(self):
            return "PROFANITY_EXPERIMENTAL"
    PROFANITY_EXPERIMENTAL = PROFANITY_EXPERIMENTAL()
    class THREAT_EXPERIMENTAL:
        """
        ## THREAT_EXPERIMENTAL
        Describes an intention to inflict pain, injury, or violence against an individual or group.

        ### Important notes on using experimental attributes:

         - Once experimental attributes are deprecated and production attributes are created, the experimental attribute will stop working. When that happens, you will need to update the API call's attribute name to the new production attribute name.
        
         - Expect language availability to change over time as we test attribute performance and move attributes to production.

        """
        description = "Describes an intention to inflict pain, injury, or violence against an individual or group."
        isExperimental = True
        def __repr__(self):
            return "THREAT_EXPERIMENTAL"
    THREAT_EXPERIMENTAL = THREAT_EXPERIMENTAL()
    class SEXUALLY_EXPLICIT:
        """
        ## SEXUALLY_EXPLICIT
        Contains references to sexual acts, body parts, or other lewd content.

        ### Important notes on using experimental attributes:

         - Once experimental attributes are deprecated and production attributes are created, the experimental attribute will stop working. When that happens, you will need to update the API call's attribute name to the new production attribute name.
        
         - Expect language availability to change over time as we test attribute performance and move attributes to production.

        """
        description = "Contains references to sexual acts, body parts, or other lewd content."
        isExperimental = True
        def __repr__(self):
            return "SEXUALLY_EXPLICIT"
    SEXUALLY_EXPLICIT = SEXUALLY_EXPLICIT()
    class FLIRTATION:
        """
        ## FLIRTATION
        Pickup lines, complimenting appearance, subtle sexual innuendos, etc.

        ### Important notes on using experimental attributes:

         - Once experimental attributes are deprecated and production attributes are created, the experimental attribute will stop working. When that happens, you will need to update the API call's attribute name to the new production attribute name.
        
         - Expect language availability to change over time as we test attribute performance and move attributes to production.

        """
        description = "Pickup lines, complimenting appearance, subtle sexual innuendos, etc."
        isExperimental = True
        def __repr__(self):
            return "FLIRTATION"
    FLIRTATION = FLIRTATION()
    
    # New York Times attributes
    class ATTACK_ON_AUTHOR:
        """
        ## ATTACK_ON_AUTHOR
        Attack on the author of an article or post.

        ### Supported language(s)

        English (en)
        """
        supportedLanguages = ["en"]
        description = "Attack on the author of an article or post."
        isExperimental = True
        def __repr__(self):
            return "ATTACK_ON_AUTHOR"
    ATTACK_ON_AUTHOR = ATTACK_ON_AUTHOR()
    class ATTACK_ON_COMMENTER:
        """
        ## ATTACK_ON_COMMENTER
        Attack on fellow commenter.

        ### Supported language(s)

        English (en)
        """
        supportedLanguages = ["en"]
        description = "Attack on fellow commenter."
        isExperimental = True
        def __repr__(self):
            return "ATTACK_ON_COMMENTER"
    ATTACK_ON_COMMENTER = ATTACK_ON_COMMENTER()
    class INCOHERENT:
        """
        ## INCOHERENT
        Difficult to understand, nonsensical.

        ### Supported language(s)

        English (en)
        """
        supportedLanguages = ["en"]
        description = "Difficult to understand, nonsensical."
        isExperimental = True
        def __repr__(self):
            return "INCOHERENT"
    INCOHERENT = INCOHERENT()
    class INFLAMMATORY:
        """
        ## INFLAMMATORY
        Intending to provoke or inflame.

        ### Supported language(s)

        English (en)
        """
        supportedLanguages = ["en"]
        description = "Intending to provoke or inflame."
        isExperimental = True
        def __repr__(self):
            return "INFLAMMATORY"
    INFLAMMATORY = INFLAMMATORY()
    class LIKELY_TO_REJECT:
        """
        ## LIKELY_TO_REJECT
        Overall measure of the likelihood for the comment to be rejected according to the NYT's moderation.

        ### Supported language(s)

        English (en)
        """
        supportedLanguages = ["en"]
        description = "Overall measure of the likelihood for the comment to be rejected according to the NYT's moderation."
        isExperimental = True
        def __repr__(self):
            return "LIKELY_TO_REJECT"
    LIKELY_TO_REJECT = LIKELY_TO_REJECT()
    class OBSCENE:
        """
        ## OBSCENE
        Obscene or vulgar language such as cursing.

        ### Supported language(s)

        English (en)
        """
        supportedLanguages = ["en"]
        description = "Obscene or vulgar language such as cursing."
        isExperimental = True
        def __repr__(self):
            return "OBSCENE"
    OBSCENE = OBSCENE()
    class SPAM:
        """
        ## SPAM
        Irrelevant and unsolicited commercial content.

        ### Supported language(s)

        English (en)
        """
        supportedLanguages = ["en"]
        description = "Irrelevant and unsolicited commercial content."
        isExperimental = True
        def __repr__(self):
            return "SPAM"
    SPAM = SPAM()
    class UNSUBSTANTIAL:
        """
        ## UNSUBSTANTIAL
        Trivial or short comments.

        ### Supported language(s)

        English (en)
        """
        supportedLanguages = ["en"]
        description = "Trivial or short comments."
        isExperimental = True
        def __repr__(self):
            return "UNSUBSTANTIAL"
    UNSUBSTANTIAL = UNSUBSTANTIAL()
all_attr_grps = [Attributes.All, Attributes.Production, Attributes.Experimental, Attributes.NewYorkTimes]
