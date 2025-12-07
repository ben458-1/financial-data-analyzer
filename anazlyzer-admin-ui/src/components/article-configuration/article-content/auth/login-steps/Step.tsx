// Step.tsx
import React from 'react';
import { Form, Input, Button, Typography, Card } from 'antd';

const { Text } = Typography;

interface StepProps {
    name: number;
    fieldKey: number;
    remove: (index: number) => void;
    form: any;
    editMode: boolean;
}

const Step: React.FC<StepProps> = ({ name, fieldKey, remove, form, editMode }) => {
    const stepTitle = form.getFieldValue(['steps', name, 'stepName']) || 'Unnamed';

    return (
        <Card
            size="small"
            title={<Text strong>Step {name + 1} - {stepTitle}</Text>}
            style={{
                minWidth: 280,
                flex: '0 0 auto',
                borderRadius: 10,
                borderColor: '#e0e0e0',
                boxShadow: '0 2px 6px rgba(0, 0, 0, 0.05)',
                position: 'relative'
            }}
        >
            {editMode && (
                <Button
                    danger
                    size="small"
                    type="link"
                    onClick={() => remove(name)}
                    style={{ position: 'absolute', top: 8, right: 8 }}
                >
                    Delete
                </Button>
            )}

            <Form.Item name={[name, 'stepName']} label="Step Name">
                <Input placeholder="e.g., email" />
            </Form.Item>
            <Form.Item name={[name, 'name']} label="Selector">
                <Input />
            </Form.Item>
            <Form.Item name={[name, 'type']} label="Selector Type">
                <Input />
            </Form.Item>
            <Form.Item name={[name, 'action']} label="Action">
                <Input />
            </Form.Item>
            <Form.Item name={[name, 'elementType']} label="Element Type">
                <Input />
            </Form.Item>
        </Card>
    );
};

export default Step;
