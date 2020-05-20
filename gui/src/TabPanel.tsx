import React from 'react';
import {makeStyles, Theme} from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Box from '@material-ui/core/Box';
import HomeIcon from '@material-ui/icons/Home';
import MoodIcon from '@material-ui/icons/Mood';
import ListAltIcon from '@material-ui/icons/ListAlt';
import AirplanemodeActiveIcon from '@material-ui/icons/AirplanemodeActive';
import MyLocationIcon from '@material-ui/icons/MyLocation';
import LanguageIcon from '@material-ui/icons/Language';
import TrendingUpIcon from '@material-ui/icons/TrendingUp';
import Home from './components/Home/Home';
import SentimentAnalysis from './components/SentimentAnalysis/SentimentAnalysis';
import Sentiment from './components/Sentiment/Sentiment';
import UserTracker from './components/UserTracker/UserTracker';
import Movement from './components/Movement/Movement';
import Statistics from './components/Statistics/Statistics';
import Language from './components/Language/Language';

interface TabPanelProps {
    children?: React.ReactNode;
    index: any;
    value: any;
}

function TabPanel(props: TabPanelProps) {
    const {children, value, index, ...other} = props;

    return (
        <div
            role='tabpanel'
            hidden={value !== index}
            id={`scrollable-force-tabpanel-${index}`}
            aria-labelledby={`scrollable-force-tab-${index}`}
            {...other}>
            {value === index && (
                <Box p={1}>
                    <div className={'container'}>
                        <div>{children}</div>
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
    const [value, setValue] = React.useState(2);

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
                    <Tab label="Home" icon={<HomeIcon/>} {...a11yProps(0)} />
                    <Tab label="Sentiment" icon={<MoodIcon/>} {...a11yProps(1)} />
                    <Tab label="Sentiment Analysis" icon={<ListAltIcon/>} {...a11yProps(2)} />
                    <Tab label="Movement" icon={<AirplanemodeActiveIcon/>} {...a11yProps(3)} />
                    <Tab label="User Tracker" icon={<MyLocationIcon/>} {...a11yProps(4)} />
                    <Tab label="Language" icon={<LanguageIcon/>} {...a11yProps(5)} />
                    <Tab label="Statistics" icon={<TrendingUpIcon/>} {...a11yProps(6)} />
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
