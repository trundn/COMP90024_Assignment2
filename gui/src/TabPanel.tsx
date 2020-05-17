import React from 'react';
import {makeStyles, Theme} from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import PhoneIcon from '@material-ui/icons/Phone';
import FavoriteIcon from '@material-ui/icons/Favorite';
import PersonPinIcon from '@material-ui/icons/PersonPin';
import HelpIcon from '@material-ui/icons/Help';
import ShoppingBasket from '@material-ui/icons/ShoppingBasket';
import ThumbDown from '@material-ui/icons/ThumbDown';
import ThumbUp from '@material-ui/icons/ThumbUp';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';
import Home from "./components/Home";
import SentimentAnalysis from "./components/SentimentAnalysis";
import Sentiment from "./components/Sentiment";
import Movement from "./components/Movement";
import UserTracker from "./components/UserTracker";
import Statistics from "./components/Statistics";
import Language from "./components/Language";

interface TabPanelProps {
    children?: React.ReactNode;
    index: any;
    value: any;
}

function TabPanel(props: TabPanelProps) {
    const {children, value, index, ...other} = props;

    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            id={`scrollable-force-tabpanel-${index}`}
            aria-labelledby={`scrollable-force-tab-${index}`}
            {...other}>
            {value === index && (
                <Box p={1}>
                    <div className={"container"}>
                        <Typography>{children}</Typography>
                    </div>
                </Box>
            )}
        </div>
    );
}

function a11yProps(index: any) {
    return {
        id: `scrollable-force-tab-${index}`,
        'aria-controls': `scrollable-force-tabpanel-${index}`,
    };
}

const useStyles = makeStyles((theme: Theme) => ({
    root: {
        flexGrow: 1,
        width: '100%',
        backgroundColor: theme.palette.background.paper,
    },
}));

export default function ScrollableTabsButtonForce() {
    const classes = useStyles();
    const [value, setValue] = React.useState(0);

    const handleChange = (event: React.ChangeEvent<{}>, newValue: number) => {
        setValue(newValue);
    };

    return (
        <div className={classes.root}>
            <AppBar position="static" color="default">
                <Tabs
                    value={value}
                    onChange={handleChange}
                    centered={true}
                    scrollButtons="on"
                    indicatorColor="primary"
                    textColor="primary"
                    aria-label="scrollable force tabs example">
                    <Tab label="Home" icon={<PhoneIcon/>} {...a11yProps(0)} />
                    <Tab label="Sentiment" icon={<FavoriteIcon/>} {...a11yProps(1)} />
                    <Tab label="Sentiment Analysis" icon={<PersonPinIcon/>} {...a11yProps(2)} />
                    <Tab label="Movement" icon={<HelpIcon/>} {...a11yProps(3)} />
                    <Tab label="User Tracker" icon={<ShoppingBasket/>} {...a11yProps(4)} />
                    <Tab label="Language" icon={<ThumbDown/>} {...a11yProps(5)} />
                    <Tab label="Statistics" icon={<ThumbUp/>} {...a11yProps(6)} />
                </Tabs>
            </AppBar>
            <TabPanel value={value} index={0}>
                <Home/>
            </TabPanel>
            <TabPanel value={value} index={1}>
                <Sentiment/>
            </TabPanel>
            <TabPanel value={value} index={2}>
                <SentimentAnalysis/>
            </TabPanel>
            <TabPanel value={value} index={3}>
                <Movement/>
            </TabPanel>
            <TabPanel value={value} index={4}>
                <UserTracker/>
            </TabPanel>
            <TabPanel value={value} index={5}>
                <Language/>
            </TabPanel>
            <TabPanel value={value} index={6}>
                <Statistics/>
            </TabPanel>
        </div>
    );
}
