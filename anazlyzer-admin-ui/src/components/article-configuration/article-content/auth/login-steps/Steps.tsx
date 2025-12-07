// Steps.tsx
import React from 'react';
import { Form, Button, Card } from 'antd';
import Step from './Step';

interface StepsProps {
    editMode: boolean;
    form: any;
}

const Steps: React.FC<StepsProps> = ({ editMode, form }) => {
    return (
        <Form.List name="steps">
            {(fields, { add, remove }) => (
                <>
                    <div style={{ display: 'flex', overflowX: 'auto', gap: 16, paddingBottom: 12 }}>
                        {fields.map(({ key, name, fieldKey }) => (
                            <Step
                                key={key}
                                name={name}
                                fieldKey={fieldKey}
                                remove={remove}
                                form={form}
                                editMode={editMode}
                            />
                        ))}

                        {editMode && (
                            <Card
                                size="small"
                                style={{
                                    minWidth: 280,
                                    flex: '0 0 auto',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    border: '1px dashed #aaa',
                                    borderRadius: 10,
                                    cursor: 'pointer',
                                }}
                                onClick={() => add()}
                            >
                                <Button type="dashed" block icon="➕">
                                    Add Step
                                </Button>
                            </Card>
                        )}
                    </div>
                </>
            )}
        </Form.List>
    );
};

export default Steps;
