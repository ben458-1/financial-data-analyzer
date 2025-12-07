import React, { useState } from 'react';
import { Switch, Table, Calendar, Space, Badge, TimePicker, Select, Button, Tabs, Modal } from 'antd';
import type { BadgeProps, CalendarProps } from 'antd';
import { TableOutlined, CalendarOutlined, EditOutlined, DeleteOutlined, ExclamationCircleFilled, ExclamationCircleOutlined } from '@ant-design/icons';
import Title from 'antd/lib/typography/Title';
import './css/scheduler.css';
import moment from 'moment';
import { Dayjs } from 'dayjs';
import TabPane from 'antd/lib/tabs/TabPane';
const { confirm } = Modal;

const scheduleTypes = [{ value: 'hourly', label: 'Hourly' }, { value: 'daily', label: 'Daily' }];



const getListData = (value: Dayjs) => {
    let listData: { type: string; content: string }[] = []; // Specify the type of listData
    switch (value.date()) {
        case 8:
            listData = [
                { type: 'warning', content: 'This is warning event.' },
                { type: 'success', content: 'This is usual event.' },
            ];
            break;
        case 10:
            listData = [
                { type: 'warning', content: 'This is warning event.' },
                { type: 'success', content: 'This is usual event.' },
                { type: 'error', content: 'This is error event.' },
            ];
            break;
        case 15:
            listData = [
                { type: 'warning', content: 'This is warning event' },
                { type: 'success', content: 'This is very long usual event......' },
                { type: 'error', content: 'This is error event 1.' },
                { type: 'error', content: 'This is error event 2.' },
                { type: 'error', content: 'This is error event 3.' },
                { type: 'error', content: 'This is error event 4.' },
            ];
            break;
        default:
    }
    return listData || [];
};

const getMonthData = (value: Dayjs) => {
    if (value.month() === 8) {
        return 1394;
    }
};

const showDeleteConfirm = () => {
    confirm({
        title: 'Are you sure delete this task?',
        icon: <ExclamationCircleOutlined />,
        content: 'Some descriptions',
        okText: 'Yes',
        okType: 'danger',
        cancelText: 'No',
        onOk() {
            console.log('OK');
        },
        onCancel() {
            console.log('Cancel');
        },
    });
};

const Scheduler: React.FC = () => {

    const [isTable, setIsTable] = useState(true);
    const [selectedScheduleType, setSelectedScheduleType] = useState<any | null>(null);
    const [dataSource, setDataSource] = useState([
        { key: '1', id: 1, newspaper: 'Financial Times', section: 'Markets', type: 'hourly', datetime: moment('30:00', 'mm:ss'), isActive: 1 },
        { key: '2', id: 2, newspaper: 'Financial Times', section: 'Companies Professional Services', type: 'hourly', datetime: moment('30:00', 'mm:ss'), isActive: 1 },
        { key: '3', id: 3, newspaper: 'Financial Times', section: 'Companies Retail & Consumer', type: 'hourly', datetime: moment('30:00', 'mm:ss'), isActive: 1 },
        { key: '4', id: 4, newspaper: 'Financial Times', section: 'Companies Technology Sector', type: 'hourly', datetime: moment('30:00', 'mm:ss'), isActive: 0 },
        { key: '5', id: 5, newspaper: 'Financial Times', section: 'Companies Industrial', type: 'hourly', datetime: moment('30:00', 'mm:ss'), isActive: 1 },
        { key: '6', id: 6, newspaper: 'Reuters', section: 'WORLD AT WORK HEADLINES BUSINESS', type: 'daily', datetime: moment('12:30:00', 'HH:mm:ss'), isActive: 1 },
        { key: '7', id: 7, newspaper: 'Reuters', section: 'LEGAL BUSINESS', type: 'daily', datetime: moment('12:30:00', 'HH:mm:ss'), isActive: 1 },
        { key: '8', id: 8, newspaper: 'Reuters', section: 'HEALTHCARE BUSINESS', type: 'daily', datetime: moment('12:30:00', 'HH:mm:ss'), isActive: 0 },
        { key: '9', id: 9, newspaper: 'Reuters', section: 'AUTOS BUSINESS', type: 'daily', datetime: moment('12:30:00', 'HH:mm:ss'), isActive: 1 },
        { key: '10', id: 10, newspaper: 'Reuters', section: 'RETAIL BUSINESS', type: 'daily', datetime: moment('12:30:00', 'HH:mm:ss'), isActive: 0 },

        { key: '11', id: 11, newspaper: 'CNBC', section: 'Markets', type: 'hourly', datetime: moment('30:00', 'mm:ss'), isActive: 1 },
        { key: '12', id: 12, newspaper: 'CNBC', section: 'Companies Professional Services', type: 'hourly', datetime: moment('30:00', 'mm:ss'), isActive: 1 },
        { key: '13', id: 13, newspaper: 'CNBC', section: 'Companies Retail & Consumer', type: 'hourly', datetime: moment('30:00', 'mm:ss'), isActive: 1 },
        { key: '14', id: 14, newspaper: 'CNBC', section: 'Companies Technology Sector', type: 'hourly', datetime: moment('30:00', 'mm:ss'), isActive: 0 },
        { key: '15', id: 15, newspaper: 'CNBC', section: 'Companies Industrial', type: 'hourly', datetime: moment('30:00', 'mm:ss'), isActive: 1 },
        { key: '16', id: 16, newspaper: 'Bloomberg', section: 'WORLD AT WORK HEADLINES BUSINESS', type: 'daily', datetime: moment('30:00', 'HH:mm:ss'), isActive: 1 },
        { key: '17', id: 17, newspaper: 'Bloomberg', section: 'LEGAL BUSINESS', type: 'daily', datetime: moment('12:30:00', 'HH:mm:ss'), isActive: 1 },
        { key: '18', id: 18, newspaper: 'Bloomberg', section: 'HEALTHCARE BUSINESS', type: 'daily', datetime: moment('12:30:00', 'HH:mm:ss'), isActive: 0 },
        { key: '19', id: 19, newspaper: 'Bloomberg', section: 'AUTOS BUSINESS', type: 'daily', datetime: moment('12:30:00', 'HH:mm:ss'), isActive: 1 },
        { key: '20', id: 20, newspaper: 'Bloomberg', section: 'RETAIL BUSINESS', type: 'daily', datetime: moment('12:30:00', 'HH:mm:ss'), isActive: 0 }
    ])

    const handleTimeChange = (datetime, timeString, rowIndex) => {
        const newData = [...dataSource];
        newData[rowIndex].datetime = datetime;
        setDataSource(newData);
        console.log('Updated time:', timeString);
    };

    const columns = [
        { title: 'Schedule ID', dataIndex: 'id', key: 'id' },
        { title: 'Newspaper', dataIndex: 'newspaper', key: 'newspaper' },
        { title: 'Section', dataIndex: 'section', key: 'section' },
        {
            title: 'Type', dataIndex: 'type', key: 'type',
            render: (value, record, index) => {
                return (
                    <span style={{ pointerEvents: 'none' }}>
                        <Select
                            defaultValue={value}
                            style={{ width: 100 }}
                        >
                            {scheduleTypes.map(option => (
                                <Select.Option key={option.value} value={option.value}>
                                    {option.label}
                                </Select.Option>
                            ))}
                        </Select>
                    </span>
                )
            }
        },
        {
            title: 'Date/Time', dataIndex: 'datetime', key: 'datetime',
            render: (value, record, index) => {
                const isDaily = record.type === 'daily';
                const format = isDaily ? 'HH:mm:ss' : 'mm:ss';

                return (
                    <span style={{ pointerEvents: 'none' }}>
                        <TimePicker
                            value={value}
                            format={isDaily ? 'HH:mm:ss' : 'mm:ss'}
                            showHour={isDaily}
                            showMinute
                            showSecond
                            onChange={(time, timeString) =>
                                handleTimeChange(time, timeString, index)
                            }
                        />
                    </span>
                )
            }

        },
        {
            title: 'Active', dataIndex: 'isActive', key: 'isActive', render: (num: number) =>
                num === 1 ? (
                    <span style={{ color: '#8cbb81', fontWeight: 500 }}>🟢 Active</span>
                ) : (
                    <span style={{ color: '#eb6c6b', fontWeight: 500 }}>🔴 Inactive</span>
                ),
        },
        {
            title: 'Action', dataIndex: 'action', key: 'action',
            render: (value, record, index) => {
                return (
                    <Space direction='horizontal'>
                        <Button
                            icon={<EditOutlined />}
                            // onClick={() => edit(record)}
                            type="link"

                        />
                        <Button
                            onClick={() => showPropsDelete}
                            icon={<DeleteOutlined />}
                            // onClick={() => edit(record)}
                            type="link"
                            danger

                        />
                    </Space>
                )
            }
        }
    ];

    // const dataSource = [

    // ];

    const monthCellRender = (value: Dayjs) => {
        const num = getMonthData(value);
        return num ? (
            <div className="notes-month">
                <section>{num}</section>
                <span>Backlog number</span>
            </div>
        ) : null;
    };

    const dateCellRender = (value: Dayjs) => {
        const listData = getListData(value);
        return (
            <ul className="events">
                {listData.map((item) => (
                    <li key={item.content}>
                        <Badge status={item.type as BadgeProps['status']} text={item.content} />
                    </li>
                ))}
            </ul>
        );
    };

    const cellRender: CalendarProps<Dayjs>['cellRender'] = (current, info) => {
        if (info.type === 'date') return dateCellRender(current);
        if (info.type === 'month') return monthCellRender(current);
        return info.originNode;
    };

    return (
        <div>
            <Space direction='vertical'>
                <Title level={4} style={{ marginTop: 5 }}>
                    <Space direction='horizontal'>
                        <span>Scraping Scheduler</span>
                        <Switch
                            checkedChildren={
                                <>

                                    {/* Table View */}
                                    <div style={{ paddingLeft: 3, paddingRight: 3 }}>
                                        <span>Table</span>
                                        <TableOutlined style={{ marginLeft: 4 }} />
                                    </div>
                                </>
                            }
                            unCheckedChildren={
                                <>

                                    {/* Calendar View */}
                                    <div style={{ paddingLeft: 3, paddingRight: 3 }}>
                                        <span>Calendar</span>
                                        <CalendarOutlined style={{ marginLeft: 4 }} />
                                    </div>
                                </>
                            }
                            checked={isTable}
                            onChange={(checked) => setIsTable(checked)}
                            className="color-switch"
                        />
                    </Space>
                </Title>
                {/* <Space style={{ marginBottom: 16 }}>
                    <Search
                        placeholder="Search by newspaper"
                        onSearch={handleSearch}
                        allowClear
                        enterButton
                        style={{ width: 300 }}
                    />
                </Space> */}
                {/* {
                    <div>
                        <span>Toggle View: </span>
                        
                    </div>
                } */}

                <div style={{ marginTop: 10 }}>
                    {isTable ? (
                        <Table bordered rowKey="id" dataSource={dataSource} columns={columns} pagination={{ pageSize: 10 }} scroll={{ x: 1200, y: 47 * 20 }} />
                    ) : (
                        <div>
                            <div style={{ paddingLeft: 24 }}>
                                <Tabs defaultActiveKey="daily">
                                    {scheduleTypes.map((sector) => (
                                        <TabPane tab={sector.label} key={sector.value}>
                                            {/* {renderArticles()} */}
                                        </TabPane>
                                    ))}
                                </Tabs>
                            </div>
                            <Calendar cellRender={cellRender} />
                        </div>
                    )}
                </div>
            </Space>
        </div>
    )
}

export default Scheduler;