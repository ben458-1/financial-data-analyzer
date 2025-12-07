import React, { useState } from 'react';
import { Card, Col, Row, Tabs, Typography } from 'antd';
import Article from '../home/ArticleView';

const { Title, Paragraph } = Typography;
const { TabPane } = Tabs;

export const articleData = [
  {
    source: "The Guardian",
    sector: "Politics",
    Headline: "UK Government Faces Backlash Over New Surveillance Laws",
    Author: "Jane Thompson",
    Date: "April 8, 2025",
    preamble: "",
    image: "https://fortune.com/img-assets/wp-content/uploads/2025/04/GettyImages-2204252217-e1744137663368.jpg?w=1440&q=75",
    body: `The UK government is under intense scrutiny after unveiling a new set of surveillance laws that critics argue infringe on basic civil liberties. The legislation, dubbed the Public Safety and Digital Oversight Act, gives sweeping powers to intelligence agencies to monitor digital communications under the guise of national security. Privacy advocates have already launched legal challenges, calling the measures "draconian" and warning of potential abuse. Prime Minister Rishi Patel defended the bill, citing the rising threat of cyber terrorism. The opposition, however, is demanding immediate amendments to protect citizen rights...`
  },
  {
    source: "Reuters",
    sector: "Finance",
    Headline: "Wall Street Tumbles as Inflation Concerns Resurface",
    Author: "Michael Gray",
    Date: "April 9, 2025",
    preamble: "",
    image: "https://bsmedia.business-standard.com/_media/bs/img/article/2024-09/29/full/1727598515-5448.jpg?im=FeatureCrop,size=(826,465)",
    body: `Brian MoranStaff Writer 
 Six Atlanta business partners think there's money in offering family values on the Internet. 
 Accelerated Growth Partners LLC has teamed up with a New York financial group to invest $7 million in two Atlanta Internet companies that market to the mainstream American family. 
 Trusted Net Inc. and ParentNet Inc. will merge to form Trusted Net Media Inc. after an infusion of capital from Accelerated Growth Partners and Kirlin Securities Inc., the major subsidiary of Kirlin Holding Corp. [Nasdaq: KILN]. 
 The merger's goal is to market Trusted Net's family-oriented, filtered Internet access to working parents who use ParentNet's service to observe their children at day care over the Internet. 
 Trusted Net is a service provider that blocks out pornographic and violent content on the Internet for its residential and commercial customers. It was formed in 1996 by David Huffman. ParentNet operates KinderCam, a service that lets parents observe their children at day-care centers. ParentNet was formed in 1996 by Christine Steinberg. 
 Jim Garrett, the lead investor of Accelerated Growth Partners, will serve as CEO of Trusted Net Media. The founders of Trusted Net and ParentNet still head the operations of the businesses they began. 
 Garrett said Trusted Net Media will gain an edge in the market for filtered Internet service providers because of the presence of KinderCam in child-care centers. 
 Trusted Net Media installs the necessary camera equipment for such centers in exchange for the exclusive rights to market KinderCam to those parents. KinderCam costs $19.95 a month. That fee, however, is cut in half if parents buy Trusted Net's Internet access for $19.95 a month. 
 If parents purchase KinderCam, they have an incentive to become Trusted Net customers, Garrett said. 
 "You could never attract $7 million to invest in just a filtered ISP or just KinderCam," Garrett said. "By putting them together, you have a cost advantage and a marketing infrastructure." 
 The company will spend $15,000 per child-care center to install the required cameras and wiring. Garrett said KinderCam will profit from advertising it will sell on the Web site that working parents use to keep on eye on their children. KinderCam can guarantee advertisers that parents will return repeatedly to the same advertising medium. 
 "The value of the Internet today centers around highly sticky applications -- something that assures advertisers that you'll go to that site. We'll have the sticky site of someone's 3-year-old at preschool," Garrett said. 
 Miles Russ, Internet analyst with The Robinson-Humphrey Co., applauded the ideas behind KinderCam and the merger with Trusted Net's Internet service. 
 "That's exactly the kind of functionality or utilitarian application of the Internet that will work," Russ said. "We are always looking for applications of the Internet that are a little bit ahead of mainstream adoption." 
 Trusted Net Media will spend $2 million over the next few months to market Trusted Net as the name brand of filtered Internet service providers for families, said Emery Ellinger, a partner with Accelerated Growth Partners and an executive vice president of Trusted Net Media. 
 Trusted Net's Internet service is now in 39 metropolitan markets. 
 Trusted Net, with 500 corporate accounts, also serves businesses that wish to limit their employees' access to the Web. The idea is to reduce liability for sexual harassment cases caused by inappropriate material from the Internet and boost productivity by not allowing employees to trade stocks while at work. 
 Ellinger said Trusted Net now has 2,000 residential customers. However, the company intends to have 250,000 subscribers of Trusted Net or KinderCam a year from now. 
 By year end, KinderCam will operate in 124 child-care centers. The company's business plan projects those numbers will reach 2,100 by the end of 2001. Each day-care center generates $1,500 of monthly revenue. 
 Trusted Net Media has shown interest in acquiring KinderCam's competition, including KinderView.com, a product of San Diego-based Cyber-Signs Inc., Garrett said. 
 Trusted Net's filtered Internet service faces about eight national competitors, said Bruce Carter, a North Carolina Web developer who has studied content management Internet service providers. 
 Carter said Trusted Net has positioned itself as a leader because it has not promoted itself as a religious business such as Rated-G Online, a product of Christian Internet directory 711.NET Inc. 
 "When you get involved in religion, it tends to limit your market," Carter said. "Trusted Net is marketing itself to mainstream America." 
 Garrett said Trusted Net Media, which has 30 employees at its Norcross office, is breaking even financially. The company plans to go public in September 2000, and to reach profitability early in 2001.`
  },
  {
    source: "Wired",
    sector: "Tech",
    Headline: "Apple Unveils First Foldable iPhone at Spring Event",
    Author: "Arjun Patel",
    Date: "April 8, 2025",
    preamble: "",
    image: "https://fortune.com/img-assets/wp-content/uploads/2025/04/GettyImages-546264317-e1744110043475.jpg?w=1440&q=75",
    body: `In a much-anticipated move, Apple has officially entered the foldable phone market with its new iPhone Flex. Revealed at the company’s annual Spring event, the device features a 7.1-inch OLED display that folds seamlessly without a visible crease, thanks to Apple’s proprietary hinge design. CEO Tim Cook touted the product as "a revolution in mobility and power." The base model starts at $1,799 and comes with the latest A18 Pro chip and dual battery architecture. Early hands-on reviews are positive, highlighting the improved multitasking experience and new gesture controls. However, critics question the long-term durability of the screen and its high price point...`
  },
  {
    source: "BBC",
    sector: "Lifestyle",
    Headline: "Minimalist Living Gains Popularity Among Gen Z",
    Author: "Alicia Moore",
    Date: "April 6, 2025",
    preamble: "",
    image: "https://fortune.com/img-assets/wp-content/uploads/2024/09/BMW_Factory_View.jpg?w=1440&q=75",
    body: `A growing number of Gen Z individuals are embracing minimalist lifestyles, driven by environmental concerns, economic pressures, and a desire for mental clarity. Social media platforms like TikTok and Instagram are flooded with content showcasing tiny homes, capsule wardrobes, and decluttered living spaces. Experts attribute this shift to a cultural pivot away from materialism. "This generation values experiences and sustainability over possessions," says sociologist Dr. Lisa Reynolds. Brands have taken notice too—companies like IKEA and Patagonia have launched minimalist-focused product lines to cater to this emerging demographic...`
  },
  {
    source: "Al Jazeera",
    sector: "Politics",
    Headline: "Global Leaders Meet in Geneva to Discuss Climate Refugee Crisis",
    Author: "Sami Akhtar",
    Date: "April 7, 2025",
    preamble: "",
    image: "https://fortune.com/img-assets/wp-content/uploads/2025/04/GettyImages-2194358551-e1744037498714.jpg?w=1440&q=75",
    body: `Delegates from over 70 nations gathered in Geneva this week to tackle the escalating crisis of climate-induced displacement. With rising sea levels, prolonged droughts, and intensifying storms uprooting communities worldwide, the UN estimates that over 143 million people could become climate refugees by 2050. The summit focused on crafting a unified international response, including legal protections and funding mechanisms. However, tensions flared as developing nations accused wealthier countries of inaction. "The global south is bearing the brunt of a crisis it didn’t cause," said Kenya’s representative. Discussions are ongoing with hopes of reaching a binding agreement by Friday...`
  },
  {
    source: "CNBC",
    sector: "Finance",
    Headline: "Bitcoin Surges Past $80,000 Amid ETF Frenzy",
    Author: "Tom Reed",
    Date: "April 9, 2025",
    preamble: "",
    image: "https://fortune.com/img-assets/wp-content/uploads/2025/04/GettyImages-2154693291-e1744059047545.jpg?w=1440&q=75",
    body: `Bitcoin hit a new all-time high of $80,212 on Tuesday as demand surged following the approval of several spot Bitcoin ETFs by the U.S. Securities and Exchange Commission. The landmark decision, hailed as a turning point for crypto adoption, has opened the floodgates for institutional investors. Analysts predict Bitcoin could reach $100,000 within the next few months if momentum continues. Ethereum and other altcoins also rallied, with ETH climbing 12% and Solana gaining 18%. While bullish investors celebrate, some experts warn of speculative bubbles and regulatory uncertainties ahead...`
  },
  {
    source: "NPR",
    sector: "Lifestyle",
    Headline: "Why More Americans Are Choosing to Go Car-Free",
    Author: "Becky Chan",
    Date: "April 8, 2025",
    preamble: "",
    image: "https://fortune.com/img-assets/wp-content/uploads/2025/04/GettyImages-1843202244-e1744109877280.jpg?w=1440&q=75",
    body: `Across major U.S. cities, a new trend is emerging: the car-free lifestyle. Motivated by rising fuel costs, urban congestion, and environmental concerns, many Americans—especially younger adults—are giving up personal vehicles altogether. Cities like Portland, Austin, and Minneapolis have seen a sharp increase in bike commuters and public transit users. Local governments are responding with expanded bike lanes, pedestrian-only zones, and electric bus fleets. "It’s liberating and saves me a ton," says 27-year-old Brooklyn resident Carlos Rivera. Critics argue that car-free living remains impractical outside urban cores, but momentum for change is clearly growing...`
  },
  {
    source: "Bloomberg",
    sector: "Tech",
    Headline: "AI-Generated Music Goes Mainstream With Grammy Nomination",
    Author: "Leah Kim",
    Date: "April 6, 2025",
    preamble: "",
    image: "https://fortune.com/img-assets/wp-content/uploads/2025/04/GettyImages-2181259843-e1744069337225.jpg?w=1440&q=75",
    body: `For the first time in history, a fully AI-generated track has been nominated for a Grammy. The song "Echoes of Tomorrow," created using DeepMuse—an advanced generative AI platform—has taken the industry by storm. Produced without human composition or vocals, the track blends orchestral depth with futuristic electronic elements. Industry veterans are divided; some celebrate the innovation, while others fear it may devalue human creativity. "It’s a new frontier, and we’re all navigating uncharted waters," said Grammy board member Carla Bennett. The nomination has sparked debates about authorship, copyright, and the future of musical expression...`
  },
  {
    source: "CNN",
    sector: "Politics",
    Headline: "U.S. Supreme Court To Hear Landmark AI Regulation Case",
    Author: "Joshua Tan",
    Date: "April 9, 2025",
    preamble: "",
    image: "https://fortune.com/img-assets/wp-content/uploads/2025/02/GettyImages-2179354875-1-e1739359280323.jpg?w=1440&q=75",
    body: `In what’s being called a landmark legal showdown, the U.S. Supreme Court will hear arguments this week over the federal government's power to regulate artificial intelligence systems. The case centers around the AI Accountability Act of 2024, which imposes safety and transparency standards on high-risk AI models. Tech giants argue the law stifles innovation and violates free speech, while government officials say it’s essential to prevent algorithmic discrimination and systemic harm. Legal scholars say the ruling could reshape the future of AI governance globally, setting a precedent for democracies wrestling with the ethical challenges of emerging technologies...`
  },
  {
    source: "Vice",
    sector: "Multimedia",
    Headline: "Virtual Reality Journalism Is Redefining the Newsroom",
    Author: "Emily Ruiz",
    Date: "April 7, 2025",
    preamble: "",
    image: "https://fortune.com/img-assets/wp-content/uploads/2025/04/GettyImages-2197414186-e1744197798174.jpg?w=1440&q=75",
    body: `Marla DialAustin Business Journal Staff 
 Highpoint Technologies Inc., an Austin company that makes data recovery software, has been acquired by the world's fastest-growing high tech exporter, Utah-based PowerQuest Corp. 
 Highpoint is a 12-person company founded in 1995 by University of Texas professor Roy Jenevein and his wife, Lucille. PowerQuest, a storage device management company based in Orem, currently has more than 200 employees. 
 In addition to its recent technology export accolade from World Trade Magazine, PowerQuest is one of the nation's five fastest-growing software companies. 
 The Highpoint buyout is PowerQuest's first acquisition. 
 Financial terms of the deal were not disclosed, but the local company is being redubbed PowerQuest-Austin. Lucille Jenevein has been named director of business development for the merged companies, while Roy Jenevein will become PowerQuest's chief technology officer and is joining the company's executive committee. 
 The couple will split their time between Orem and Austin, but the rest of Highpoint's employees will remain in Austin. 
 Executives say the buy presents opportunities for both companies. For Highpoint, it's access to new sales channels; for PowerQuest, technology that enhances its existing products. 
 "We are very strong in the retail channel, which is an enviable position for any software market," says Candice Steelman, vice president of corporate communications for PowerQuest. 
 She says Highpoint's direct sales model has some advantages, because "you get a better margin that way, but you don't get the depth and breadth the retail channel will give you." 
 Now, Highpoint will be part of a company with its own value-added reseller program, an office in Germany, sales associates around the globe and the ability to publish software in five languages. 
 Meanwhile, Highpoint's data protection technology dovetails nicely into PowerQuest's products and "enhance what we're doing in the enterprise solutions arena," Steelman says. 
 "This is one of those acquisitions -- we've got huge smiles on our faces, on both sides," Lucille Jenevein says. 
 Analyst Philip Mendoza of International Data Corp. says the acquisition means PowerQuest is moving into new markets. 
 "People often use PowerQuest's products to do system recovery," he says. "That means that if you're sitting at your PC and it crashes ... [technicians] would come in, maybe take your computer away and repair the system so it works again." 
 The problem is, repairing a system doesn't guarantee users get their data back. That's where Highpoint -- whose first product is called Databack -- comes in, retrieving the information that has been lost from the disk drive. 
 Although Highpoint has been approached by other would-be buyers in recent months, Lucille Jenevein says the company hit it off when executives met with PowerQuest employees at a trade show last year. 
 "Most acquisitions fail because the cultures are not similar, and that's the first thing you pay attention to, the culture of the companies. It's uncanny how [Highpoint and PowerQuest] think -- we finish each other's sentences." 
 Lucille Jenevein has seen a number of acquisitions during her sales career, which includes 16 years with companies such as Digital Equipment Corp., Sun Microsystems and IBM. Roy Jenevein is a software author and computer science professor who wrote UT's patent for optical bus technology. 
 Lucille Jenevein says the couple "got the wild hair" to start their own business three years ago. 
 While still keeping his other projects in the fire, Roy spent nights and weekends writing code for Databack. Lucille left IBM a year later, and the product finally began shipping at the end of 1996. 
 "It was a struggle for a year and a half," Lucille Jenevein recalls. "We jumped off the deep end. I had no idea there were rocks in that pool." 
 Databack is software that automates the data retrieval process, which normally is difficult and costly, Lucille Jenevein says. Highpoint's customers now include companies such as Microsoft, General Motors and Motorola, and Jenevein says Databack likely will generate nearly $1 million in sales by the end of this year. 
 Shortly before the PowerQuest purchase, Highpoint struck an exclusive deal with Western Digital Corp. The disk drive maker agreed to use only Highpoint's software in its internal data retrieval operations, and to sell it with all its own disk drives. 
 "1999 is the year I would have said would really be the year for us," Lucille Jenevein says. 
 With that kind of momentum on its own, why should Highpoint welcome the acquisition? 
 "Synergies," she says. "The two companies are phenomenally alike. We've got so much technology in their heads, they've got technology in their heads ... We communicate with these people so well. It's a natural fit." 
 PowerQuest plans to release Highpoint's existing products globally under its own name. 
 Individual products already under way will be merged within the new company, but no product release dates have been set, Steelman says.`
  }
];


const sectors = ['Home', 'Tech', 'Finance', 'Politics', 'Lifestyle', 'Multimedia'];

const Home: React.FC = () => {
  const [selectedArticle, setSelectedArticle] = useState<any | null>(null);

  const renderArticles = () => (
    <Row gutter={[16, 16]}>
      {articleData.map((article, index) => (
        <Col span={8} key={index}>
          <Card
            hoverable
            onClick={() => setSelectedArticle(article)}
            style={{ borderRadius: 12 }}
          >
            <Title level={5}>{article.Headline}</Title>
            <Paragraph type="secondary">{article.Author} - {article.source}</Paragraph>
            <Paragraph>{article.Date}</Paragraph>
          </Card>
        </Col>
      ))}
    </Row>
  );

  return (
    <div style={{ padding: 24 }}>
      {selectedArticle ? (
        <Article article={selectedArticle} onBack={() => setSelectedArticle(null)} />
      ) : (
        <>
          <Tabs defaultActiveKey="Home">
            {sectors.map((sector) => (
              <TabPane tab={sector} key={sector}>
                {renderArticles()}
              </TabPane>
            ))}
          </Tabs>
        </>
      )}
    </div>
  );
};

export default Home;
