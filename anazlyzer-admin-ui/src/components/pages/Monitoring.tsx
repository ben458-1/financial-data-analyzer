import { Space, Table, Tag, Timeline, ConfigProvider } from "antd";
import Title from "antd/lib/typography/Title";
import React, { useState } from "react";
import { LoadingOutlined } from '@ant-design/icons';

const Monitoring: React.FC = () => {
  const [dataSource, setDataSource] = useState([
    {
      key: '1', id: 1, newspaper: 'Financial Times', section: 'Markets', datetimeStart: 'May 7, 2025 9:00:36 PM', currentStatus: 'In Queue', activityLog: [
        { type: "green", value: "Sent to queue." }
      ], datetimeEnd: ''
    },
    {
      key: '2', id: 2, newspaper: 'Financial Times', section: 'Markets', datetimeStart: 'May 7, 2025 8:59:21 PM', currentStatus: 'Ongoing', activityLog: [
        { type: "green", value: "Sent to queue." },
        { type: "#eac000", value: "Gathering article metadatas..." }
      ], datetimeEnd: ''
    },
    {
      key: '3', id: 3, newspaper: 'Financial Times', section: 'Markets', datetimeStart: 'May 7, 2025 8:59:02 PM', currentStatus: 'Ongoing', activityLog: [
        { type: "green", value: "Sent to queue." },
        { type: "green", value: "Gathering article metadatas..." },
        { type: "blue", value: "Processing 56 article metadatas..." }
      ], datetimeEnd: ''
    },
    {
      key: '4', id: 4, newspaper: 'Financial Times', section: 'Markets', datetimeStart: 'May 7, 2025 8:58:59 PM', currentStatus: 'Ongoing', activityLog: [
        { type: "green", value: "Sent to queue." },
        { type: "green", value: "Gathering article metadatas..." },
        { type: "green", value: "Processing 103 article metadatas..." },
        { type: "green", value: "Successfully processed 103 article metadatas. Total of 50 new articles." },
        { type: "blue", value: "Gathering article contents..." }
      ], datetimeEnd: ''
    },
    {
      key: '5', id: 5, newspaper: 'Financial Times', section: 'Markets', datetimeStart: 'May 7, 2025 8:59:53 PM', currentStatus: 'Ongoing', activityLog: [
        { type: "green", value: "Sent to queue." },
        { type: "green", value: "Gathering article metadatas..." },
        { type: "green", value: "Processing 121 article metadatas..." },
        { type: "green", value: "Successfully processed 121 article metadatas. Total of 115 new articles." },
        { type: "green", value: "Gathering 115 article contents..." },
        { type: "green", value: "Processing 115 article contents..." }
      ], datetimeEnd: ''
    },
    {
      key: '6', id: 6, newspaper: 'Financial Times', section: 'Markets', datetimeStart: 'May 6, 2025 7:00:01 PM', currentStatus: 'Finished', activityLog: [
        { type: "green", value: "Sent to queue." },
        { type: "green", value: "Gathering article metadatas..." },
        { type: "green", value: "Processing 29 article metadatas..." },
        { type: "green", value: "Successfully processed 29 article metadatas. Total of 15 new articles." },
        { type: "green", value: "Gathering 15 article contents..." },
        { type: "green", value: "Processing 15 article contents..." },
        { type: "green", value: "Successfully processed 15 article contents." },
        { type: "green", value: "Sent to AI queue for further processing." }
      ], datetimeEnd: 'May 6, 2025 7:02:25 PM'
    },
    {
      key: '7', id: 7, newspaper: 'Financial Times', section: 'Markets', datetimeStart: 'May 6, 2025 6:58:12 PM', currentStatus: 'Failed', activityLog: [
        { type: "green", value: "Sent to queue." },
        { type: "green", value: "Gathering article metadatas..." },
        { type: "green", value: "Processing 29 article metadatas..." },
        { type: "green", value: "Successfully processed 29 article metadatas. Total of 15 new articles." },
        { type: "green", value: "Gathering 15 article contents..." },
        { type: "orange", value: "There was an unexpected issue. Retrying (1)..." },
        { type: "orange", value: "There was an unexpected issue. Retrying (2)..." },
        { type: "orange", value: "There was an unexpected issue. Retrying (3)..." },
        { type: "red", value: "Failed. Error message has been sent to [alec.sison@euroland.com, vigneshwaran@euroland.com] for diagnosis." }
      ], datetimeEnd: 'May 6, 2025 6:59:31 PM'
    },
    {
      key: '8', id: 8, newspaper: 'Financial Times', section: 'Markets', datetimeStart: 'May 5, 2025 04:31:02 PM', currentStatus: 'Finished', activityLog: [
        { type: "green", value: "Sent to queue." },
        { type: "green", value: "Gathering article metadatas..." },
        { type: "green", value: "Processing 35 article metadatas..." },
        { type: "green", value: "Successfully processed 35 article metadatas. Total of 35 new articles." },
        { type: "green", value: "Gathering 35 article contents..." },
        { type: "green", value: "Processing 35 article contents..." },
        { type: "green", value: "Successfully processed 35 article contents." },
        { type: "green", value: "Sent to AI queue for further processing." }
      ], datetimeEnd: 'May 5, 2025 04:32:52 PM'
    },
    {
      key: '9', id: 9, newspaper: 'Financial Times', section: 'Markets', datetimeStart: 'May 5, 2025 04:29:51 PM', currentStatus: 'Finished', activityLog: [
        { type: "green", value: "Sent to queue." },
        { type: "green", value: "Gathering article metadatas..." },
        { type: "green", value: "Processing 71 article metadatas..." },
        { type: "green", value: "Successfully processed 71 article metadatas. Total of 71 new articles." },
        { type: "green", value: "Gathering 71 article contents..." },
        { type: "green", value: "Processing 71 article contents..." },
        { type: "green", value: "Successfully processed 71 article contents." },
        { type: "green", value: "Sent to AI queue for further processing." }
      ], datetimeEnd: 'May 5, 2025 04:31:01 PM'
    },
    {
      key: '10', id: 10, newspaper: 'Financial Times', section: 'Markets', datetimeStart: 'May 5, 2025 04:25:05 PM', currentStatus: 'Finished', activityLog: [
        { type: "green", value: "Sent to queue." },
        { type: "green", value: "Gathering article metadatas..." },
        { type: "green", value: "Processing 85 article metadatas..." },
        { type: "green", value: "Successfully processed 85 article metadatas. Total of 85 new articles." },
        { type: "green", value: "Gathering 85 article contents..." },
        { type: "green", value: "Processing 85 article contents..." },
        { type: "green", value: "Successfully processed 85 article contents." },
        { type: "green", value: "Sent to AI queue for further processing." }
      ], datetimeEnd: 'May 5, 2025 04:26:35 PM'
    },
  ])

  const columns = [
    // { title: 'Task ID', dataIndex: 'id', key: 'id'},
    { title: 'Newspaper', dataIndex: 'newspaper', key: 'newspaper' },
    { title: 'Section', dataIndex: 'section', key: 'section' },
    ,
    { title: 'Datetime Started', dataIndex: 'datetimeStart', key: 'datetimeStart', width: '15%', },
    ,
    {
      title: 'Current Status', dataIndex: 'currentStatus', key: 'currentStatus',
      render: (value) => {
        let color = ''

        if (value === 'Ongoing') color = 'yellow'
        else if (value === 'Failed') color = 'red'
        else if (value === 'In Queue') color = 'orange'
        else color = 'green'
        return (
          // <Space direction="horizontal">
          //   <div
          //     style={{
          //       width: '12px',
          //       height: '12px',
          //       borderRadius: '50%',
          //       backgroundColor: 'white', // Ongoing status will be gray
          //       border: '2px solid #eac000', // optional: add a border for visibility
          //     }}
          //   /><span> Ongoing</span>
          // </Space>
          <Tag color={color} key={value} style={{ fontWeight: 600 }}>
            {value.toUpperCase()}
          </Tag>
        )
      }
    },
    {
      title: 'Activity Log', dataIndex: 'activityLog', key: 'activityLog', width: '35%',
      render: (activityLog) => (
        <Timeline mode="left" >
          {activityLog.map((log, index) => (
            <Timeline.Item key={index} color={log.type} style={{paddingBottom: '2px'}}>
              {log.value}
            </Timeline.Item>
          ))}
        </Timeline>
      )
    },
    {
      title: 'Datetime Ended', dataIndex: 'datetimeEnd', key: 'datetimeEnd', width: '15%'
    }

  ];

  return (
    <div>
      <Space direction='vertical'>
        <Title level={4} style={{ marginTop: 5 }}>
          <span>Monitoring Page</span>
        </Title>

        <Table rowKey="id" dataSource={dataSource} columns={columns} pagination={{ pageSize: 10 }} scroll={{ x: 1200, y: 47 * 20 }} />
      </Space>
    </div>
  );
};

export default Monitoring;
