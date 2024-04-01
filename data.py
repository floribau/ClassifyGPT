import pandas as pd
import random

# Dataset consisting of 50 test samples.
# They are classified into one of 25 category paths, each category path having two samples.
test_dataset = pd.read_csv('icecat_test_data.csv')

# Label lists and definition for each label as specified by Icecat
SECOND_LEVEL_LABELS = ['Computers', 'Warranty & Support', 'Software', 'TVs & Monitors', 'Data Input Devices',
                       'Computer Cables', 'Telecom & Navigation', 'Batteries & Power Supplies', 'Projectors',
                       'Networking']

THIRD_LEVEL_LABELS = ['Notebooks', 'Warranty & Support Extensions', 'Software Licenses/Upgrades', 'PCs/Workstations',
                      'TVs', 'Keyboards', 'All-in-One PCs/Workstations', 'Computer Monitors', 'Networking Cables',
                      'Antivirus Security Software', 'Mobile Phone Cases', 'Power Adapters & Inverters',
                      'Flat Panel Spare Parts', 'Fibre Optic Cables', 'Smartphones', 'Tablets', 'Projection Screens',
                      'Screen Protectors', 'Tablet Cases', 'Uninterruptible Power Supplies (UPSs)',
                      'Cable Interface/Gender Adapters', 'Data Projectors', 'Network Switches', 'Mice', 'Power Cables']

LABEL_DEFINITIONS = {
    'Computers': "Electronic devices capable of receiving, processing, and storing data to perform various tasks. "
                 "Computers encompass a wide range of devices, including desktops, laptops, tablets, and servers. "
                 "They consist of hardware components such as processors, memory (RAM), storage, input/output "
                 "devices, and often include software systems like operating systems and applications for user "
                 "interaction and task execution. Computers are used for purposes such as personal productivity, "
                 "entertainment, communication, and data processing across various domains.",
    'Warranty & Support': "A warranty is a written guarantee, issued to the purchaser of an article by its "
                          "manufacturer, promising to repair or replace it if necessary within a specified period of "
                          "time. Support means help with set-up and use of a device, and if there are any problems "
                          "with it.",
    'Software': "Instructions for a computer's processor to perform specific operations e.g. system software such as "
                "Windows and iOS, application software such as internet browsers and apps.",
    'TVs & Monitors': "Television sets and computer displays used for visual entertainment or as output devices for "
                      "computers. TVs receive and display broadcast signals, while monitors are specifically designed "
                      "for computer output.",
    'Data Input Devices': "Input devices that allow for user inputs to a computer, e.g., keyboard and joystick.",
    'Computer Cables': "Cables used to connect computers to power supplies and other devices such as printers.",
    'Telecom & Navigation': "Portable computer devices and phones, and their accessories such as cables and stands.",
    'Batteries & Power Supplies': "Battery units and devices used to power electronic equipment, providing portable "
                                  "energy sources for various devices. Power supplies include units that convert "
                                  "electrical power from one form to another to ensure proper operation of electronic "
                                  "devices.",
    'Projectors': "Device that is used to project rays of light, especially an apparatus with a system of lenses for "
                  "projecting slides or film on to a screen.",
    'Networking': "A telecommunications network which allows computers and other electronic devices to exchange data. "
                  "Common examples are local area networks (LANs) and virtual private networks (VPNs).",
    'Notebooks': "Portable computing devices, designed for mobility and convenience. Notebooks integrate components "
                 "such as a display screen, keyboard, processor, memory, and storage into a single compact unit.",
    'Warranty & Support Extensions': "Extending the warranty & support beyond that offered by the "
                                     "manufacturer/retailer, so that the purchase is covered for a longer period of "
                                     "time.",
    'Software Licenses/Upgrades': "A software licence permits you to use a piece of software legally. An software "
                                  "upgrade is a newer or better version, in order to bring the software up to date or "
                                  "to improve its characteristics.",
    'PCs/Workstations': "Personal Computers, PCs for short, are computers for personal usage. They always have the "
                        "following components: a processor (CPU), memory (RAM), motherboard, video board, "
                        "a hard disk, and an optional DVD/CD player/recorder.",
    'TVs': "Television sets designed for receiving and displaying broadcasted visual content, including programs, "
           "movies, and video games. TVs come in various sizes, display technologies, and feature sets (such as smart "
           "capabilities, resolution, and refresh rate).",
    'Keyboards': "The keyboard is the main input peripheral used by all computers. The keyboard allows for user input "
                 "and interaction with the computer.",
    'All-in-One PCs/Workstations': "Desktop PC with monitor.",
    'Computer Monitors': "TFT/LCD displays are perfectly flat, a lot thinner and lighter than conventional CRT "
                         "displays and do not flicker, all this because of the new technology they use for producing "
                         "images. Do you want to free up space on your desk, or do you want to be able to move your "
                         "monitor without breaking your back? Then this is the perfect display for you!",
    'Networking Cables': "Any type of network has its own type of cables. Today's standard for home and office use is "
                         "Ethernet. For Fast Ethernet and Gigabit Ethernet you need at least category 5 cabling. "
                         "Ethernet cables can have their connectors attached in two different ways: ordinary or cross "
                         "linked. You will most likely need the ordinary version, unless you want to connect two "
                         "devices directly to each other, and even then most modern Ethernet network devices will "
                         "automatically detect the type of cable you are using and adapt their settings to it, "
                         "so they will work with both types.",
    'Antivirus Security Software': "Computer programs that protect computer systems, files and software from computer "
                                   "viruses, etc.",
    'Mobile Phone Cases': "Telecom & Navigation>Mobile Phone Cases: Protective cases for mobile phones such as "
                          "smartphones.",
    'Power Adapters & Inverters': "A power adapter connects a device into the mains electricity through a plug. They "
                                  "are used with  electrical devices that require power but do not contain internal "
                                  "components to derive the required voltage and power from mains power. A power "
                                  "inverter, or inverter, is an electronic device or circuitry that changes direct "
                                  "current (DC) to alternating current (AC).",
    'Flat Panel Spare Parts': "Replacement components and spare parts for flat-panel TVs and monitors, including "
                              "items such as screens, circuit boards, and connectors.",
    'Fibre Optic Cables': "A thin glass fibre through which light can be transmitted.",
    'Smartphones': "Mobile phone that is able to perform many of the functions of a computer, typically having a "
                   "relatively large screen and an operating system capable of running general-purpose applications.",
    'Tablets': "Mobile computer with display, circuitry and battery in a single unit. Tablets are equipped with "
               "sensors, including cameras, microphone, accelerometer and touchscreen, with finger or stylus gestures "
               "replacing computer mouse and keyboard.",
    'Projection Screens': "Installation consisting of a surface and a support structure used for displaying a "
                          "projected image for the view of an audience.",
    'Screen Protectors': "Plastic covers used to protect smartphone screen from scratching etc.",
    'Tablet Cases': "Protective cases for tablets such as the iPad.",
    'Uninterruptible Power Supplies (UPSs)': "Once you have a UPS (Uninterruptible Power Supply), there is no need to "
                                             "fear for data loss due to power outages. If the duration of the outage "
                                             "is short, you can work on without being disturbed, and if it takes "
                                             "longer, you will have more than enough time to save your work and "
                                             "safely turn off your computer.",
    'Cable Interface/Gender Adapters': "Adapters used to convert between different cable interfaces or genders, "
                                       "facilitating connections between devices with incompatible connectors. These "
                                       "adapters ensure compatibility and proper signal transmission in networking, "
                                       "audiovisual, and other setups.",
    'Data Projectors': "Use a beamer to project the images from your notebook, computer, DVD-player, video recorder "
                       "or other device with a compatible connector on the wall or a specially-designed projection "
                       "screen. With a device like this, giving professional, clear presentations is easy. Or make "
                       "your own home cinema!",
    'Network Switches': "A switch is a device with which it is possible to connect computers into a (local area) "
                        "network, provided your computers all have an appropriate networking device installed. "
                        "Switches can be daisy chained to form larger networks and come in managed and unmanaged "
                        "variaties. The unmanaged versions generally cannot filter data and will forward any data "
                        "that is fed into them, so they are better suited for small networks. Switches are easy to "
                        "set up (just plug in the network cables) and allow you to share printers, storage space and "
                        "other network resources with your entire home or office network.",
    'Mice': "The mouse is the second most important way of communicating with a computer.",
    'Power Cables': "A power cable, also known as a power cord, is used for the transmission of electrical power."
}

# System Prompt explaining the general setting. This prompt will be performed before each classification
SYSTEM_PROMPT = ("You are tasked with classifying products within a hierarchical category structure consisting of "
                 "three levels. All products fall under the overarching first-level category 'Computers & "
                 "Electronics.' Your role is to utilize your expertise to categorize the products effectively into "
                 "their second and third level categories, considering their attributes, intended use, and notable "
                 "features. The classification involves predicting the second-level and third-level categories from "
                 "two provided category pools. Your response should not only provide the classification path but also"
                 "explain the reasoning behind your decision. "
                 "Please provide, alongside your reasoning, your answer for the hierarchical path in the format "
                 "\"Computers & Electronics>[Second-level Category]>[Third-level Category]\". [Second-level Category] "
                 "and [Third-level Category] are placeholders for the predicted categories on the second and third "
                 "level. Only use categories from the second-level pool to fill the [Second-level Category] "
                 "placeholder. Only use categories from the third-level pool to fill the [Third-level Category] "
                 "placeholder.")

# User Prompt Templates to be filled with product and label input
USER_PROMPT_TEMPLATE_1 = ("The product to be classified is \"{title}\" of the brand {brand}.\n"
                          "Please classify the specified product into the described product hierarchy. "
                          "Fill the placeholder [Second-level Category] with a category of this second-level pool: "
                          "{label_2_1}, {label_2_2}, {label_2_3}, {label_2_4}, {label_2_5}, "
                          "{label_2_6}, {label_2_7}, {label_2_8}, {label_2_9}, {label_2_10}.\n")

USER_PROMPT_TEMPLATE_2 = ("Use the following definitions for the second-level categories:\n"
                          "- {label_2_1}: {definition_2_1}\n"
                          "- {label_2_2}: {definition_2_2}\n"
                          "- {label_2_3}: {definition_2_3}\n"
                          "- {label_2_4}: {definition_2_4}\n"
                          "- {label_2_5}: {definition_2_5}\n"
                          "- {label_2_6}: {definition_2_6}\n"
                          "- {label_2_7}: {definition_2_7}\n"
                          "- {label_2_8}: {definition_2_8}\n"
                          "- {label_2_9}: {definition_2_9}\n"
                          "- {label_2_10}: {definition_2_10}\n")

USER_PROMPT_TEMPLATE_3 = ("Fill the placeholder [Third-level Category] with a category from this third-level pool: "
                          "{label_3_1}, {label_3_2}, {label_3_3}, {label_3_4}, {label_3_5}, {label_3_6}, "
                          "{label_3_7}, {label_3_8}, {label_3_9}, {label_3_10}, {label_3_11}, {label_3_12}, "
                          "{label_3_13}, {label_3_14}, {label_3_15}, {label_3_16}, {label_3_17}, {label_3_18}, "
                          "{label_3_19}, {label_3_20}, {label_3_21}, {label_3_22}, {label_3_23}, {label_3_24}, "
                          "{label_3_25}. It is highly important that you only use categories from the third-level pool "
                          "to fill the [Third-level Category] placeholder.\n")

USER_PROMPT_TEMPLATE_4 = ("Use the following definitions for the third-level categories:\n"
                          "- {label_3_1}: {definition_3_1}\n"
                          "- {label_3_2}: {definition_3_2}\n"
                          "- {label_3_3}: {definition_3_3}\n"
                          "- {label_3_4}: {definition_3_4}\n"
                          "- {label_3_5}: {definition_3_5}\n"
                          "- {label_3_6}: {definition_3_6}\n"
                          "- {label_3_7}: {definition_3_7}\n"
                          "- {label_3_8}: {definition_3_8}\n"
                          "- {label_3_9}: {definition_3_9}\n"
                          "- {label_3_10}: {definition_3_10}\n"
                          "- {label_3_11}: {definition_3_11}\n"
                          "- {label_3_12}: {definition_3_12}\n"
                          "- {label_3_13}: {definition_3_13}\n"
                          "- {label_3_14}: {definition_3_14}\n"
                          "- {label_3_15}: {definition_3_15}\n"
                          "- {label_3_16}: {definition_3_16}\n"
                          "- {label_3_17}: {definition_3_17}\n"
                          "- {label_3_18}: {definition_3_18}\n"
                          "- {label_3_19}: {definition_3_19}\n"
                          "- {label_3_20}: {definition_3_20}\n"
                          "- {label_3_21}: {definition_3_21}\n"
                          "- {label_3_22}: {definition_3_22}\n"
                          "- {label_3_23}: {definition_3_23}\n"
                          "- {label_3_24}: {definition_3_24}\n"
                          "- {label_3_25}: {definition_3_25}\n")

USER_PROMPT_TEMPLATE_5 = ("It is crucial that the answer path exactly matches the three-level hierarchy format "
                          "\"Computers & Electronics>[Second-level Category]>[Third-level Category]\"."
                          "Only answers with the correct number of levels and the correct path format can be accepted."
                          "The format needs to follow the example \"Computers & Electronics>Data Input "
                          "Devices>Keyboards\"")


def format_user_prompt(title: str, brand: str, second_level_labels: list[str], third_level_labels: list[str],
                       with_definition: bool = False) -> str:
    """
    Assembles the user prompt templates and fills it with the given specifications.

    :param title: Title of the product
    :param brand: Brand of the product
    :param second_level_labels: List of second-level categories, either in original or in permuted order
    :param third_level_labels: List of third-level categories, either in original or in permuted order
    :param with_definition: Adds label definitions if True, doesn't add label definitions if False
    :return: Formatted string for the user prompt
    """
    labels = {f"label_2_{i}": second_level_labels[i - 1] for i in range(1, 11)}
    labels.update({f"label_3_{i}": third_level_labels[i - 1] for i in range(1, 26)})

    definitions = {f"definition_2_{i}": LABEL_DEFINITIONS[labels[f"label_2_{i}"]] for i in range(1, 11)}
    definitions.update({f"definition_3_{i}": LABEL_DEFINITIONS[labels[f"label_3_{i}"]] for i in range(1, 26)})

    if with_definition:
        user_prompt_template = (USER_PROMPT_TEMPLATE_1 + USER_PROMPT_TEMPLATE_2 + USER_PROMPT_TEMPLATE_3 +
                                USER_PROMPT_TEMPLATE_4 + USER_PROMPT_TEMPLATE_5)
        formatted_string = user_prompt_template.format(title=title, brand=brand, **labels, **definitions)
    else:
        user_prompt_template = USER_PROMPT_TEMPLATE_1 + USER_PROMPT_TEMPLATE_3 + USER_PROMPT_TEMPLATE_5

        formatted_string = user_prompt_template.format(title=title, brand=brand, **labels)
    return formatted_string


def permute_labels(labels: list[str]) -> list[str]:
    """
    Randomly permutes a list of labels.

    :param labels: list of labels in original order
    :return: a copy of the labels list with permuted order
    """
    permuted_labels = labels[:]
    random.shuffle(permuted_labels)
    return permuted_labels
