# AWS Resource Type Support in CrowdStrike

This table shows which AWS Config resource types are supported by CrowdStrike for custom IOM rules.

## Summary

- **Total Tested**: 413 resource types
- **Supported**: 128 (31.0%)
- **Not Supported**: 285 (69.0%)
- **Last Updated**: 2025-12-03T15:50:15Z

## Resource Type Support Table

| Resource Type | CrowdStrike Support | AWS Config Schema |
|---------------|-------------------|------------------|
| `AWS::ACM::Certificate` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AACM%3A%3ACertificate.properties.json) |
| `AWS::ACMPCA::CertificateAuthority` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AACMPCA%3A%3ACertificateAuthority.properties.json) |
| `AWS::ACMPCA::CertificateAuthorityActivation` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AACMPCA%3A%3ACertificateAuthorityActivation.properties.json) |
| `AWS::APS::RuleGroupsNamespace` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAPS%3A%3ARuleGroupsNamespace.properties.json) |
| `AWS::AccessAnalyzer::Analyzer` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAccessAnalyzer%3A%3AAnalyzer.properties.json) |
| `AWS::AmazonMQ::Broker` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAmazonMQ%3A%3ABroker.properties.json) |
| `AWS::Amplify::App` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAmplify%3A%3AApp.properties.json) |
| `AWS::Amplify::Branch` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAmplify%3A%3ABranch.properties.json) |
| `AWS::ApiGateway::RestApi` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AApiGateway%3A%3ARestApi.properties.json) |
| `AWS::ApiGateway::Stage` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AApiGateway%3A%3AStage.properties.json) |
| `AWS::ApiGatewayV2::Api` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AApiGatewayV2%3A%3AApi.properties.json) |
| `AWS::ApiGatewayV2::Stage` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AApiGatewayV2%3A%3AStage.properties.json) |
| `AWS::AppConfig::Application` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAppConfig%3A%3AApplication.properties.json) |
| `AWS::AppConfig::ConfigurationProfile` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAppConfig%3A%3AConfigurationProfile.properties.json) |
| `AWS::AppConfig::DeploymentStrategy` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAppConfig%3A%3ADeploymentStrategy.properties.json) |
| `AWS::AppConfig::Environment` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAppConfig%3A%3AEnvironment.properties.json) |
| `AWS::AppConfig::ExtensionAssociation` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAppConfig%3A%3AExtensionAssociation.properties.json) |
| `AWS::AppConfig::HostedConfigurationVersion` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAppConfig%3A%3AHostedConfigurationVersion.properties.json) |
| `AWS::AppFlow::Flow` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAppFlow%3A%3AFlow.properties.json) |
| `AWS::AppIntegrations::EventIntegration` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAppIntegrations%3A%3AEventIntegration.properties.json) |
| `AWS::AppMesh::GatewayRoute` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAppMesh%3A%3AGatewayRoute.properties.json) |
| `AWS::AppMesh::Mesh` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAppMesh%3A%3AMesh.properties.json) |
| `AWS::AppMesh::Route` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAppMesh%3A%3ARoute.properties.json) |
| `AWS::AppMesh::VirtualGateway` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAppMesh%3A%3AVirtualGateway.properties.json) |
| `AWS::AppMesh::VirtualNode` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAppMesh%3A%3AVirtualNode.properties.json) |
| `AWS::AppMesh::VirtualRouter` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAppMesh%3A%3AVirtualRouter.properties.json) |
| `AWS::AppMesh::VirtualService` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAppMesh%3A%3AVirtualService.properties.json) |
| `AWS::AppRunner::Service` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAppRunner%3A%3AService.properties.json) |
| `AWS::AppRunner::VpcConnector` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAppRunner%3A%3AVpcConnector.properties.json) |
| `AWS::AppStream::Application` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAppStream%3A%3AApplication.properties.json) |
| `AWS::AppStream::DirectoryConfig` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAppStream%3A%3ADirectoryConfig.properties.json) |
| `AWS::AppStream::Fleet` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAppStream%3A%3AFleet.properties.json) |
| `AWS::AppStream::Stack` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAppStream%3A%3AStack.properties.json) |
| `AWS::AppSync::GraphQLApi` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAppSync%3A%3AGraphQLApi.properties.json) |
| `AWS::Athena::DataCatalog` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAthena%3A%3ADataCatalog.properties.json) |
| `AWS::Athena::PreparedStatement` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAthena%3A%3APreparedStatement.properties.json) |
| `AWS::Athena::WorkGroup` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAthena%3A%3AWorkGroup.properties.json) |
| `AWS::AuditManager::Assessment` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAuditManager%3A%3AAssessment.properties.json) |
| `AWS::AutoScaling::AutoScalingGroup` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAutoScaling%3A%3AAutoScalingGroup.properties.json) |
| `AWS::AutoScaling::LaunchConfiguration` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAutoScaling%3A%3ALaunchConfiguration.properties.json) |
| `AWS::AutoScaling::ScalingPolicy` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAutoScaling%3A%3AScalingPolicy.properties.json) |
| `AWS::AutoScaling::ScheduledAction` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAutoScaling%3A%3AScheduledAction.properties.json) |
| `AWS::AutoScaling::WarmPool` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AAutoScaling%3A%3AWarmPool.properties.json) |
| `AWS::Backup::BackupPlan` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ABackup%3A%3ABackupPlan.properties.json) |
| `AWS::Backup::BackupSelection` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ABackup%3A%3ABackupSelection.properties.json) |
| `AWS::Backup::BackupVault` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ABackup%3A%3ABackupVault.properties.json) |
| `AWS::Backup::RecoveryPoint` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ABackup%3A%3ARecoveryPoint.properties.json) |
| `AWS::Backup::ReportPlan` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ABackup%3A%3AReportPlan.properties.json) |
| `AWS::Batch::ComputeEnvironment` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ABatch%3A%3AComputeEnvironment.properties.json) |
| `AWS::Batch::JobQueue` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ABatch%3A%3AJobQueue.properties.json) |
| `AWS::Batch::SchedulingPolicy` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ABatch%3A%3ASchedulingPolicy.properties.json) |
| `AWS::Budgets::BudgetsAction` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ABudgets%3A%3ABudgetsAction.properties.json) |
| `AWS::Cassandra::Keyspace` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ACassandra%3A%3AKeyspace.properties.json) |
| `AWS::Cloud9::EnvironmentEC2` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ACloud9%3A%3AEnvironmentEC2.properties.json) |
| `AWS::CloudFormation::Stack` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ACloudFormation%3A%3AStack.properties.json) |
| `AWS::CloudFront::Distribution` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ACloudFront%3A%3ADistribution.properties.json) |
| `AWS::CloudFront::StreamingDistribution` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ACloudFront%3A%3AStreamingDistribution.properties.json) |
| `AWS::CloudTrail::Trail` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ACloudTrail%3A%3ATrail.properties.json) |
| `AWS::CloudWatch::Alarm` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ACloudWatch%3A%3AAlarm.properties.json) |
| `AWS::CloudWatch::MetricStream` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ACloudWatch%3A%3AMetricStream.properties.json) |
| `AWS::CodeArtifact::Repository` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ACodeArtifact%3A%3ARepository.properties.json) |
| `AWS::CodeBuild::Project` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ACodeBuild%3A%3AProject.properties.json) |
| `AWS::CodeBuild::ReportGroup` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ACodeBuild%3A%3AReportGroup.properties.json) |
| `AWS::CodeDeploy::Application` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ACodeDeploy%3A%3AApplication.properties.json) |
| `AWS::CodeDeploy::DeploymentConfig` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ACodeDeploy%3A%3ADeploymentConfig.properties.json) |
| `AWS::CodeDeploy::DeploymentGroup` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ACodeDeploy%3A%3ADeploymentGroup.properties.json) |
| `AWS::CodeGuruProfiler::ProfilingGroup` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ACodeGuruProfiler%3A%3AProfilingGroup.properties.json) |
| `AWS::CodeGuruReviewer::RepositoryAssociation` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ACodeGuruReviewer%3A%3ARepositoryAssociation.properties.json) |
| `AWS::CodePipeline::Pipeline` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ACodePipeline%3A%3APipeline.properties.json) |
| `AWS::Cognito::IdentityPool` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ACognito%3A%3AIdentityPool.properties.json) |
| `AWS::Cognito::UserPoolClient` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ACognito%3A%3AUserPoolClient.properties.json) |
| `AWS::Cognito::UserPoolGroup` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ACognito%3A%3AUserPoolGroup.properties.json) |
| `AWS::Config::ConfigurationRecorder` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AConfig%3A%3AConfigurationRecorder.properties.json) |
| `AWS::Config::ConformancePackCompliance` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AConfig%3A%3AConformancePackCompliance.properties.json) |
| `AWS::Config::ResourceCompliance` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AConfig%3A%3AResourceCompliance.properties.json) |
| `AWS::Connect::Instance` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AConnect%3A%3AInstance.properties.json) |
| `AWS::Connect::PhoneNumber` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AConnect%3A%3APhoneNumber.properties.json) |
| `AWS::Connect::QuickConnect` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AConnect%3A%3AQuickConnect.properties.json) |
| `AWS::CustomerProfiles::Domain` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ACustomerProfiles%3A%3ADomain.properties.json) |
| `AWS::CustomerProfiles::ObjectType` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ACustomerProfiles%3A%3AObjectType.properties.json) |
| `AWS::DMS::Certificate` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ADMS%3A%3ACertificate.properties.json) |
| `AWS::DMS::Endpoint` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ADMS%3A%3AEndpoint.properties.json) |
| `AWS::DMS::EventSubscription` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ADMS%3A%3AEventSubscription.properties.json) |
| `AWS::DMS::ReplicationInstance` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ADMS%3A%3AReplicationInstance.properties.json) |
| `AWS::DMS::ReplicationSubnetGroup` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ADMS%3A%3AReplicationSubnetGroup.properties.json) |
| `AWS::DMS::ReplicationTask` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ADMS%3A%3AReplicationTask.properties.json) |
| `AWS::DataSync::LocationEFS` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ADataSync%3A%3ALocationEFS.properties.json) |
| `AWS::DataSync::LocationFSxLustre` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ADataSync%3A%3ALocationFSxLustre.properties.json) |
| `AWS::DataSync::LocationFSxWindows` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ADataSync%3A%3ALocationFSxWindows.properties.json) |
| `AWS::DataSync::LocationHDFS` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ADataSync%3A%3ALocationHDFS.properties.json) |
| `AWS::DataSync::LocationNFS` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ADataSync%3A%3ALocationNFS.properties.json) |
| `AWS::DataSync::LocationObjectStorage` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ADataSync%3A%3ALocationObjectStorage.properties.json) |
| `AWS::DataSync::LocationS3` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ADataSync%3A%3ALocationS3.properties.json) |
| `AWS::DataSync::LocationSMB` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ADataSync%3A%3ALocationSMB.properties.json) |
| `AWS::DataSync::Task` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ADataSync%3A%3ATask.properties.json) |
| `AWS::Detective::Graph` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ADetective%3A%3AGraph.properties.json) |
| `AWS::DeviceFarm::InstanceProfile` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ADeviceFarm%3A%3AInstanceProfile.properties.json) |
| `AWS::DeviceFarm::Project` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ADeviceFarm%3A%3AProject.properties.json) |
| `AWS::DeviceFarm::TestGridProject` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ADeviceFarm%3A%3ATestGridProject.properties.json) |
| `AWS::DynamoDB::Table` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ADynamoDB%3A%3ATable.properties.json) |
| `AWS::EC2::CapacityReservation` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3ACapacityReservation.properties.json) |
| `AWS::EC2::CarrierGateway` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3ACarrierGateway.properties.json) |
| `AWS::EC2::ClientVpnEndpoint` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3AClientVpnEndpoint.properties.json) |
| `AWS::EC2::CustomerGateway` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3ACustomerGateway.properties.json) |
| `AWS::EC2::DHCPOptions` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3ADHCPOptions.properties.json) |
| `AWS::EC2::EC2Fleet` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3AEC2Fleet.properties.json) |
| `AWS::EC2::EIP` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3AEIP.properties.json) |
| `AWS::EC2::EgressOnlyInternetGateway` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3AEgressOnlyInternetGateway.properties.json) |
| `AWS::EC2::FlowLog` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3AFlowLog.properties.json) |
| `AWS::EC2::Host` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3AHost.properties.json) |
| `AWS::EC2::IPAM` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3AIPAM.properties.json) |
| `AWS::EC2::IPAMPool` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3AIPAMPool.properties.json) |
| `AWS::EC2::IPAMScope` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3AIPAMScope.properties.json) |
| `AWS::EC2::Instance` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3AInstance.properties.json) |
| `AWS::EC2::InternetGateway` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3AInternetGateway.properties.json) |
| `AWS::EC2::LaunchTemplate` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3ALaunchTemplate.properties.json) |
| `AWS::EC2::NatGateway` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3ANatGateway.properties.json) |
| `AWS::EC2::NetworkAcl` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3ANetworkAcl.properties.json) |
| `AWS::EC2::NetworkInsightsAccessScope` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3ANetworkInsightsAccessScope.properties.json) |
| `AWS::EC2::NetworkInsightsAccessScopeAnalysis` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3ANetworkInsightsAccessScopeAnalysis.properties.json) |
| `AWS::EC2::NetworkInsightsPath` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3ANetworkInsightsPath.properties.json) |
| `AWS::EC2::NetworkInterface` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3ANetworkInterface.properties.json) |
| `AWS::EC2::PrefixList` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3APrefixList.properties.json) |
| `AWS::EC2::RegisteredHAInstance` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3ARegisteredHAInstance.properties.json) |
| `AWS::EC2::RouteTable` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3ARouteTable.properties.json) |
| `AWS::EC2::SecurityGroup` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3ASecurityGroup.properties.json) |
| `AWS::EC2::SpotFleet` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3ASpotFleet.properties.json) |
| `AWS::EC2::Subnet` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3ASubnet.properties.json) |
| `AWS::EC2::SubnetRouteTableAssociation` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3ASubnetRouteTableAssociation.properties.json) |
| `AWS::EC2::TrafficMirrorFilter` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3ATrafficMirrorFilter.properties.json) |
| `AWS::EC2::TrafficMirrorSession` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3ATrafficMirrorSession.properties.json) |
| `AWS::EC2::TrafficMirrorTarget` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3ATrafficMirrorTarget.properties.json) |
| `AWS::EC2::TransitGateway` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3ATransitGateway.properties.json) |
| `AWS::EC2::TransitGatewayAttachment` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3ATransitGatewayAttachment.properties.json) |
| `AWS::EC2::TransitGatewayConnect` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3ATransitGatewayConnect.properties.json) |
| `AWS::EC2::TransitGatewayMulticastDomain` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3ATransitGatewayMulticastDomain.properties.json) |
| `AWS::EC2::TransitGatewayRouteTable` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3ATransitGatewayRouteTable.properties.json) |
| `AWS::EC2::VPC` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3AVPC.properties.json) |
| `AWS::EC2::VPCBlockPublicAccessExclusion` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3AVPCBlockPublicAccessExclusion.properties.json) |
| `AWS::EC2::VPCBlockPublicAccessOptions` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3AVPCBlockPublicAccessOptions.properties.json) |
| `AWS::EC2::VPCEndpoint` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3AVPCEndpoint.properties.json) |
| `AWS::EC2::VPCEndpointService` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3AVPCEndpointService.properties.json) |
| `AWS::EC2::VPCPeeringConnection` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3AVPCPeeringConnection.properties.json) |
| `AWS::EC2::VPNConnection` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3AVPNConnection.properties.json) |
| `AWS::EC2::VPNGateway` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3AVPNGateway.properties.json) |
| `AWS::EC2::Volume` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEC2%3A%3AVolume.properties.json) |
| `AWS::ECR::PublicRepository` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AECR%3A%3APublicRepository.properties.json) |
| `AWS::ECR::PullThroughCacheRule` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AECR%3A%3APullThroughCacheRule.properties.json) |
| `AWS::ECR::RegistryPolicy` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AECR%3A%3ARegistryPolicy.properties.json) |
| `AWS::ECR::Repository` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AECR%3A%3ARepository.properties.json) |
| `AWS::ECS::CapacityProvider` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AECS%3A%3ACapacityProvider.properties.json) |
| `AWS::ECS::Cluster` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AECS%3A%3ACluster.properties.json) |
| `AWS::ECS::Service` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AECS%3A%3AService.properties.json) |
| `AWS::ECS::TaskDefinition` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AECS%3A%3ATaskDefinition.properties.json) |
| `AWS::ECS::TaskSet` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AECS%3A%3ATaskSet.properties.json) |
| `AWS::EFS::AccessPoint` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEFS%3A%3AAccessPoint.properties.json) |
| `AWS::EFS::FileSystem` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEFS%3A%3AFileSystem.properties.json) |
| `AWS::EKS::Addon` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEKS%3A%3AAddon.properties.json) |
| `AWS::EKS::Cluster` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEKS%3A%3ACluster.properties.json) |
| `AWS::EKS::FargateProfile` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEKS%3A%3AFargateProfile.properties.json) |
| `AWS::EKS::IdentityProviderConfig` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEKS%3A%3AIdentityProviderConfig.properties.json) |
| `AWS::EMR::SecurityConfiguration` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEMR%3A%3ASecurityConfiguration.properties.json) |
| `AWS::ElasticBeanstalk::Application` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AElasticBeanstalk%3A%3AApplication.properties.json) |
| `AWS::ElasticBeanstalk::ApplicationVersion` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AElasticBeanstalk%3A%3AApplicationVersion.properties.json) |
| `AWS::ElasticBeanstalk::Environment` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AElasticBeanstalk%3A%3AEnvironment.properties.json) |
| `AWS::ElasticLoadBalancing::LoadBalancer` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AElasticLoadBalancing%3A%3ALoadBalancer.properties.json) |
| `AWS::ElasticLoadBalancingV2::Listener` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AElasticLoadBalancingV2%3A%3AListener.properties.json) |
| `AWS::ElasticLoadBalancingV2::LoadBalancer` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AElasticLoadBalancingV2%3A%3ALoadBalancer.properties.json) |
| `AWS::Elasticsearch::Domain` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AElasticsearch%3A%3ADomain.properties.json) |
| `AWS::EventSchemas::Discoverer` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEventSchemas%3A%3ADiscoverer.properties.json) |
| `AWS::EventSchemas::Registry` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEventSchemas%3A%3ARegistry.properties.json) |
| `AWS::EventSchemas::RegistryPolicy` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEventSchemas%3A%3ARegistryPolicy.properties.json) |
| `AWS::EventSchemas::Schema` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEventSchemas%3A%3ASchema.properties.json) |
| `AWS::Events::ApiDestination` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEvents%3A%3AApiDestination.properties.json) |
| `AWS::Events::Archive` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEvents%3A%3AArchive.properties.json) |
| `AWS::Events::Connection` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEvents%3A%3AConnection.properties.json) |
| `AWS::Events::Endpoint` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEvents%3A%3AEndpoint.properties.json) |
| `AWS::Events::EventBus` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEvents%3A%3AEventBus.properties.json) |
| `AWS::Events::Rule` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEvents%3A%3ARule.properties.json) |
| `AWS::Evidently::Launch` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEvidently%3A%3ALaunch.properties.json) |
| `AWS::Evidently::Project` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEvidently%3A%3AProject.properties.json) |
| `AWS::Evidently::Segment` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AEvidently%3A%3ASegment.properties.json) |
| `AWS::Forecast::DatasetGroup` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AForecast%3A%3ADatasetGroup.properties.json) |
| `AWS::FraudDetector::EntityType` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AFraudDetector%3A%3AEntityType.properties.json) |
| `AWS::FraudDetector::Label` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AFraudDetector%3A%3ALabel.properties.json) |
| `AWS::FraudDetector::Outcome` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AFraudDetector%3A%3AOutcome.properties.json) |
| `AWS::FraudDetector::Variable` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AFraudDetector%3A%3AVariable.properties.json) |
| `AWS::GlobalAccelerator::Accelerator` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AGlobalAccelerator%3A%3AAccelerator.properties.json) |
| `AWS::GlobalAccelerator::EndpointGroup` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AGlobalAccelerator%3A%3AEndpointGroup.properties.json) |
| `AWS::GlobalAccelerator::Listener` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AGlobalAccelerator%3A%3AListener.properties.json) |
| `AWS::Glue::Classifier` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AGlue%3A%3AClassifier.properties.json) |
| `AWS::Glue::Job` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AGlue%3A%3AJob.properties.json) |
| `AWS::Glue::MLTransform` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AGlue%3A%3AMLTransform.properties.json) |
| `AWS::GreengrassV2::ComponentVersion` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AGreengrassV2%3A%3AComponentVersion.properties.json) |
| `AWS::GroundStation::Config` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AGroundStation%3A%3AConfig.properties.json) |
| `AWS::GroundStation::DataflowEndpointGroup` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AGroundStation%3A%3ADataflowEndpointGroup.properties.json) |
| `AWS::GroundStation::MissionProfile` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AGroundStation%3A%3AMissionProfile.properties.json) |
| `AWS::GuardDuty::Detector` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AGuardDuty%3A%3ADetector.properties.json) |
| `AWS::GuardDuty::Filter` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AGuardDuty%3A%3AFilter.properties.json) |
| `AWS::IAM::Group` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIAM%3A%3AGroup.properties.json) |
| `AWS::IAM::OIDCProvider` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIAM%3A%3AOIDCProvider.properties.json) |
| `AWS::IAM::Policy` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIAM%3A%3APolicy.properties.json) |
| `AWS::IAM::Role` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIAM%3A%3ARole.properties.json) |
| `AWS::IAM::SAMLProvider` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIAM%3A%3ASAMLProvider.properties.json) |
| `AWS::IAM::ServerCertificate` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIAM%3A%3AServerCertificate.properties.json) |
| `AWS::IAM::User` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIAM%3A%3AUser.properties.json) |
| `AWS::IVS::Channel` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIVS%3A%3AChannel.properties.json) |
| `AWS::IVS::PlaybackKeyPair` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIVS%3A%3APlaybackKeyPair.properties.json) |
| `AWS::IVS::RecordingConfiguration` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIVS%3A%3ARecordingConfiguration.properties.json) |
| `AWS::ImageBuilder::ContainerRecipe` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AImageBuilder%3A%3AContainerRecipe.properties.json) |
| `AWS::ImageBuilder::DistributionConfiguration` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AImageBuilder%3A%3ADistributionConfiguration.properties.json) |
| `AWS::ImageBuilder::ImagePipeline` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AImageBuilder%3A%3AImagePipeline.properties.json) |
| `AWS::ImageBuilder::ImageRecipe` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AImageBuilder%3A%3AImageRecipe.properties.json) |
| `AWS::ImageBuilder::InfrastructureConfiguration` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AImageBuilder%3A%3AInfrastructureConfiguration.properties.json) |
| `AWS::InspectorV2::Filter` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AInspectorV2%3A%3AFilter.properties.json) |
| `AWS::IoT::AccountAuditConfiguration` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoT%3A%3AAccountAuditConfiguration.properties.json) |
| `AWS::IoT::Authorizer` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoT%3A%3AAuthorizer.properties.json) |
| `AWS::IoT::CACertificate` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoT%3A%3ACACertificate.properties.json) |
| `AWS::IoT::CustomMetric` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoT%3A%3ACustomMetric.properties.json) |
| `AWS::IoT::Dimension` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoT%3A%3ADimension.properties.json) |
| `AWS::IoT::FleetMetric` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoT%3A%3AFleetMetric.properties.json) |
| `AWS::IoT::JobTemplate` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoT%3A%3AJobTemplate.properties.json) |
| `AWS::IoT::MitigationAction` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoT%3A%3AMitigationAction.properties.json) |
| `AWS::IoT::Policy` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoT%3A%3APolicy.properties.json) |
| `AWS::IoT::ProvisioningTemplate` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoT%3A%3AProvisioningTemplate.properties.json) |
| `AWS::IoT::RoleAlias` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoT%3A%3ARoleAlias.properties.json) |
| `AWS::IoT::ScheduledAudit` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoT%3A%3AScheduledAudit.properties.json) |
| `AWS::IoT::SecurityProfile` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoT%3A%3ASecurityProfile.properties.json) |
| `AWS::IoTAnalytics::Channel` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoTAnalytics%3A%3AChannel.properties.json) |
| `AWS::IoTAnalytics::Dataset` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoTAnalytics%3A%3ADataset.properties.json) |
| `AWS::IoTAnalytics::Datastore` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoTAnalytics%3A%3ADatastore.properties.json) |
| `AWS::IoTAnalytics::Pipeline` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoTAnalytics%3A%3APipeline.properties.json) |
| `AWS::IoTEvents::AlarmModel` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoTEvents%3A%3AAlarmModel.properties.json) |
| `AWS::IoTEvents::DetectorModel` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoTEvents%3A%3ADetectorModel.properties.json) |
| `AWS::IoTEvents::Input` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoTEvents%3A%3AInput.properties.json) |
| `AWS::IoTSiteWise::AssetModel` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoTSiteWise%3A%3AAssetModel.properties.json) |
| `AWS::IoTSiteWise::Dashboard` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoTSiteWise%3A%3ADashboard.properties.json) |
| `AWS::IoTSiteWise::Gateway` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoTSiteWise%3A%3AGateway.properties.json) |
| `AWS::IoTSiteWise::Portal` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoTSiteWise%3A%3APortal.properties.json) |
| `AWS::IoTSiteWise::Project` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoTSiteWise%3A%3AProject.properties.json) |
| `AWS::IoTTwinMaker::Entity` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoTTwinMaker%3A%3AEntity.properties.json) |
| `AWS::IoTTwinMaker::Scene` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoTTwinMaker%3A%3AScene.properties.json) |
| `AWS::IoTTwinMaker::SyncJob` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoTTwinMaker%3A%3ASyncJob.properties.json) |
| `AWS::IoTTwinMaker::Workspace` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoTTwinMaker%3A%3AWorkspace.properties.json) |
| `AWS::IoTWireless::FuotaTask` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoTWireless%3A%3AFuotaTask.properties.json) |
| `AWS::IoTWireless::MulticastGroup` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoTWireless%3A%3AMulticastGroup.properties.json) |
| `AWS::IoTWireless::ServiceProfile` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AIoTWireless%3A%3AServiceProfile.properties.json) |
| `AWS::KMS::Alias` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AKMS%3A%3AAlias.properties.json) |
| `AWS::KMS::Key` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AKMS%3A%3AKey.properties.json) |
| `AWS::Kendra::Index` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AKendra%3A%3AIndex.properties.json) |
| `AWS::Kinesis::Stream` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AKinesis%3A%3AStream.properties.json) |
| `AWS::Kinesis::StreamConsumer` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AKinesis%3A%3AStreamConsumer.properties.json) |
| `AWS::KinesisAnalyticsV2::Application` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AKinesisAnalyticsV2%3A%3AApplication.properties.json) |
| `AWS::KinesisFirehose::DeliveryStream` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AKinesisFirehose%3A%3ADeliveryStream.properties.json) |
| `AWS::KinesisVideo::SignalingChannel` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AKinesisVideo%3A%3ASignalingChannel.properties.json) |
| `AWS::KinesisVideo::Stream` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AKinesisVideo%3A%3AStream.properties.json) |
| `AWS::Lambda::CodeSigningConfig` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ALambda%3A%3ACodeSigningConfig.properties.json) |
| `AWS::Lambda::Function` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ALambda%3A%3AFunction.properties.json) |
| `AWS::Lex::Bot` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ALex%3A%3ABot.properties.json) |
| `AWS::Lex::BotAlias` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ALex%3A%3ABotAlias.properties.json) |
| `AWS::Lightsail::Bucket` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ALightsail%3A%3ABucket.properties.json) |
| `AWS::Lightsail::Certificate` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ALightsail%3A%3ACertificate.properties.json) |
| `AWS::Lightsail::Disk` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ALightsail%3A%3ADisk.properties.json) |
| `AWS::Lightsail::StaticIp` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ALightsail%3A%3AStaticIp.properties.json) |
| `AWS::Logs::Destination` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ALogs%3A%3ADestination.properties.json) |
| `AWS::LookoutVision::Project` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ALookoutVision%3A%3AProject.properties.json) |
| `AWS::M2::Environment` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AM2%3A%3AEnvironment.properties.json) |
| `AWS::MSK::BatchScramSecret` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AMSK%3A%3ABatchScramSecret.properties.json) |
| `AWS::MSK::Cluster` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AMSK%3A%3ACluster.properties.json) |
| `AWS::MSK::ClusterPolicy` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AMSK%3A%3AClusterPolicy.properties.json) |
| `AWS::MSK::Configuration` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AMSK%3A%3AConfiguration.properties.json) |
| `AWS::MSK::VpcConnection` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AMSK%3A%3AVpcConnection.properties.json) |
| `AWS::MediaConnect::FlowSource` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AMediaConnect%3A%3AFlowSource.properties.json) |
| `AWS::MediaConnect::FlowVpcInterface` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AMediaConnect%3A%3AFlowVpcInterface.properties.json) |
| `AWS::MediaConnect::Gateway` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AMediaConnect%3A%3AGateway.properties.json) |
| `AWS::MediaPackage::PackagingConfiguration` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AMediaPackage%3A%3APackagingConfiguration.properties.json) |
| `AWS::MediaPackage::PackagingGroup` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AMediaPackage%3A%3APackagingGroup.properties.json) |
| `AWS::MediaTailor::PlaybackConfiguration` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AMediaTailor%3A%3APlaybackConfiguration.properties.json) |
| `AWS::MemoryDB::SubnetGroup` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AMemoryDB%3A%3ASubnetGroup.properties.json) |
| `AWS::NetworkFirewall::Firewall` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ANetworkFirewall%3A%3AFirewall.properties.json) |
| `AWS::NetworkFirewall::FirewallPolicy` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ANetworkFirewall%3A%3AFirewallPolicy.properties.json) |
| `AWS::NetworkFirewall::RuleGroup` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ANetworkFirewall%3A%3ARuleGroup.properties.json) |
| `AWS::NetworkFirewall::TLSInspectionConfiguration` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ANetworkFirewall%3A%3ATLSInspectionConfiguration.properties.json) |
| `AWS::NetworkManager::ConnectPeer` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ANetworkManager%3A%3AConnectPeer.properties.json) |
| `AWS::NetworkManager::CustomerGatewayAssociation` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ANetworkManager%3A%3ACustomerGatewayAssociation.properties.json) |
| `AWS::NetworkManager::Device` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ANetworkManager%3A%3ADevice.properties.json) |
| `AWS::NetworkManager::GlobalNetwork` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ANetworkManager%3A%3AGlobalNetwork.properties.json) |
| `AWS::NetworkManager::Link` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ANetworkManager%3A%3ALink.properties.json) |
| `AWS::NetworkManager::LinkAssociation` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ANetworkManager%3A%3ALinkAssociation.properties.json) |
| `AWS::NetworkManager::Site` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ANetworkManager%3A%3ASite.properties.json) |
| `AWS::NetworkManager::TransitGatewayRegistration` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ANetworkManager%3A%3ATransitGatewayRegistration.properties.json) |
| `AWS::OpenSearch::Domain` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AOpenSearch%3A%3ADomain.properties.json) |
| `AWS::OpenSearchServerless::VpcEndpoint` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AOpenSearchServerless%3A%3AVpcEndpoint.properties.json) |
| `AWS::Panorama::Package` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3APanorama%3A%3APackage.properties.json) |
| `AWS::Personalize::Dataset` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3APersonalize%3A%3ADataset.properties.json) |
| `AWS::Personalize::DatasetGroup` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3APersonalize%3A%3ADatasetGroup.properties.json) |
| `AWS::Personalize::Schema` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3APersonalize%3A%3ASchema.properties.json) |
| `AWS::Personalize::Solution` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3APersonalize%3A%3ASolution.properties.json) |
| `AWS::Pinpoint::App` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3APinpoint%3A%3AApp.properties.json) |
| `AWS::Pinpoint::ApplicationSettings` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3APinpoint%3A%3AApplicationSettings.properties.json) |
| `AWS::Pinpoint::Campaign` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3APinpoint%3A%3ACampaign.properties.json) |
| `AWS::Pinpoint::EmailChannel` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3APinpoint%3A%3AEmailChannel.properties.json) |
| `AWS::Pinpoint::EmailTemplate` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3APinpoint%3A%3AEmailTemplate.properties.json) |
| `AWS::Pinpoint::EventStream` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3APinpoint%3A%3AEventStream.properties.json) |
| `AWS::Pinpoint::InAppTemplate` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3APinpoint%3A%3AInAppTemplate.properties.json) |
| `AWS::Pinpoint::Segment` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3APinpoint%3A%3ASegment.properties.json) |
| `AWS::QLDB::Ledger` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AQLDB%3A%3ALedger.properties.json) |
| `AWS::QuickSight::DataSource` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AQuickSight%3A%3ADataSource.properties.json) |
| `AWS::RDS::DBCluster` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARDS%3A%3ADBCluster.properties.json) |
| `AWS::RDS::DBClusterSnapshot` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARDS%3A%3ADBClusterSnapshot.properties.json) |
| `AWS::RDS::DBInstance` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARDS%3A%3ADBInstance.properties.json) |
| `AWS::RDS::DBSecurityGroup` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARDS%3A%3ADBSecurityGroup.properties.json) |
| `AWS::RDS::DBSnapshot` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARDS%3A%3ADBSnapshot.properties.json) |
| `AWS::RDS::DBSubnetGroup` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARDS%3A%3ADBSubnetGroup.properties.json) |
| `AWS::RDS::EventSubscription` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARDS%3A%3AEventSubscription.properties.json) |
| `AWS::RDS::GlobalCluster` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARDS%3A%3AGlobalCluster.properties.json) |
| `AWS::RDS::OptionGroup` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARDS%3A%3AOptionGroup.properties.json) |
| `AWS::RUM::AppMonitor` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARUM%3A%3AAppMonitor.properties.json) |
| `AWS::Redshift::Cluster` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARedshift%3A%3ACluster.properties.json) |
| `AWS::Redshift::ClusterParameterGroup` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARedshift%3A%3AClusterParameterGroup.properties.json) |
| `AWS::Redshift::ClusterSecurityGroup` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARedshift%3A%3AClusterSecurityGroup.properties.json) |
| `AWS::Redshift::ClusterSnapshot` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARedshift%3A%3AClusterSnapshot.properties.json) |
| `AWS::Redshift::ClusterSubnetGroup` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARedshift%3A%3AClusterSubnetGroup.properties.json) |
| `AWS::Redshift::EndpointAccess` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARedshift%3A%3AEndpointAccess.properties.json) |
| `AWS::Redshift::EndpointAuthorization` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARedshift%3A%3AEndpointAuthorization.properties.json) |
| `AWS::Redshift::EventSubscription` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARedshift%3A%3AEventSubscription.properties.json) |
| `AWS::Redshift::ScheduledAction` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARedshift%3A%3AScheduledAction.properties.json) |
| `AWS::ResilienceHub::App` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AResilienceHub%3A%3AApp.properties.json) |
| `AWS::ResilienceHub::ResiliencyPolicy` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AResilienceHub%3A%3AResiliencyPolicy.properties.json) |
| `AWS::ResourceExplorer2::Index` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AResourceExplorer2%3A%3AIndex.properties.json) |
| `AWS::RoboMaker::RobotApplication` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARoboMaker%3A%3ARobotApplication.properties.json) |
| `AWS::RoboMaker::RobotApplicationVersion` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARoboMaker%3A%3ARobotApplicationVersion.properties.json) |
| `AWS::RoboMaker::SimulationApplication` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARoboMaker%3A%3ASimulationApplication.properties.json) |
| `AWS::Route53::HealthCheck` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARoute53%3A%3AHealthCheck.properties.json) |
| `AWS::Route53::HostedZone` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARoute53%3A%3AHostedZone.properties.json) |
| `AWS::Route53RecoveryControl::Cluster` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARoute53RecoveryControl%3A%3ACluster.properties.json) |
| `AWS::Route53RecoveryControl::ControlPanel` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARoute53RecoveryControl%3A%3AControlPanel.properties.json) |
| `AWS::Route53RecoveryControl::RoutingControl` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARoute53RecoveryControl%3A%3ARoutingControl.properties.json) |
| `AWS::Route53RecoveryControl::SafetyRule` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARoute53RecoveryControl%3A%3ASafetyRule.properties.json) |
| `AWS::Route53RecoveryReadiness::Cell` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARoute53RecoveryReadiness%3A%3ACell.properties.json) |
| `AWS::Route53RecoveryReadiness::ReadinessCheck` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARoute53RecoveryReadiness%3A%3AReadinessCheck.properties.json) |
| `AWS::Route53RecoveryReadiness::RecoveryGroup` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARoute53RecoveryReadiness%3A%3ARecoveryGroup.properties.json) |
| `AWS::Route53RecoveryReadiness::ResourceSet` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARoute53RecoveryReadiness%3A%3AResourceSet.properties.json) |
| `AWS::Route53Resolver::FirewallDomainList` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARoute53Resolver%3A%3AFirewallDomainList.properties.json) |
| `AWS::Route53Resolver::FirewallRuleGroup` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARoute53Resolver%3A%3AFirewallRuleGroup.properties.json) |
| `AWS::Route53Resolver::FirewallRuleGroupAssociation` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARoute53Resolver%3A%3AFirewallRuleGroupAssociation.properties.json) |
| `AWS::Route53Resolver::ResolverQueryLoggingConfig` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARoute53Resolver%3A%3AResolverQueryLoggingConfig.properties.json) |
| `AWS::Route53Resolver::ResolverQueryLoggingConfigAssociation` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARoute53Resolver%3A%3AResolverQueryLoggingConfigAssociation.properties.json) |
| `AWS::Route53Resolver::ResolverRule` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARoute53Resolver%3A%3AResolverRule.properties.json) |
| `AWS::Route53Resolver::ResolverRuleAssociation` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ARoute53Resolver%3A%3AResolverRuleAssociation.properties.json) |
| `AWS::S3::AccessPoint` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AS3%3A%3AAccessPoint.properties.json) |
| `AWS::S3::AccountPublicAccessBlock` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AS3%3A%3AAccountPublicAccessBlock.properties.json) |
| `AWS::S3::Bucket` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AS3%3A%3ABucket.properties.json) |
| `AWS::S3::MultiRegionAccessPoint` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AS3%3A%3AMultiRegionAccessPoint.properties.json) |
| `AWS::S3::StorageLens` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AS3%3A%3AStorageLens.properties.json) |
| `AWS::S3Express::BucketPolicy` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AS3Express%3A%3ABucketPolicy.properties.json) |
| `AWS::S3Express::DirectoryBucket` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AS3Express%3A%3ADirectoryBucket.properties.json) |
| `AWS::SES::ConfigurationSet` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ASES%3A%3AConfigurationSet.properties.json) |
| `AWS::SES::ContactList` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ASES%3A%3AContactList.properties.json) |
| `AWS::SES::ReceiptFilter` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ASES%3A%3AReceiptFilter.properties.json) |
| `AWS::SES::ReceiptRuleSet` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ASES%3A%3AReceiptRuleSet.properties.json) |
| `AWS::SES::Template` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ASES%3A%3ATemplate.properties.json) |
| `AWS::SNS::Topic` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ASNS%3A%3ATopic.properties.json) |
| `AWS::SQS::Queue` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ASQS%3A%3AQueue.properties.json) |
| `AWS::SSM::AssociationCompliance` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ASSM%3A%3AAssociationCompliance.properties.json) |
| `AWS::SSM::Document` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ASSM%3A%3ADocument.properties.json) |
| `AWS::SSM::FileData` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ASSM%3A%3AFileData.properties.json) |
| `AWS::SSM::ManagedInstanceInventory` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ASSM%3A%3AManagedInstanceInventory.properties.json) |
| `AWS::SSM::PatchCompliance` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ASSM%3A%3APatchCompliance.properties.json) |
| `AWS::SageMaker::AppImageConfig` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ASageMaker%3A%3AAppImageConfig.properties.json) |
| `AWS::SageMaker::CodeRepository` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ASageMaker%3A%3ACodeRepository.properties.json) |
| `AWS::SageMaker::Domain` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ASageMaker%3A%3ADomain.properties.json) |
| `AWS::SageMaker::EndpointConfig` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ASageMaker%3A%3AEndpointConfig.properties.json) |
| `AWS::SageMaker::FeatureGroup` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ASageMaker%3A%3AFeatureGroup.properties.json) |
| `AWS::SageMaker::Image` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ASageMaker%3A%3AImage.properties.json) |
| `AWS::SageMaker::Model` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ASageMaker%3A%3AModel.properties.json) |
| `AWS::SageMaker::NotebookInstance` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ASageMaker%3A%3ANotebookInstance.properties.json) |
| `AWS::SageMaker::NotebookInstanceLifecycleConfig` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ASageMaker%3A%3ANotebookInstanceLifecycleConfig.properties.json) |
| `AWS::SageMaker::Workteam` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ASageMaker%3A%3AWorkteam.properties.json) |
| `AWS::SecretsManager::Secret` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ASecretsManager%3A%3ASecret.properties.json) |
| `AWS::ServiceCatalog::CloudFormationProduct` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AServiceCatalog%3A%3ACloudFormationProduct.properties.json) |
| `AWS::ServiceCatalog::CloudFormationProvisionedProduct` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AServiceCatalog%3A%3ACloudFormationProvisionedProduct.properties.json) |
| `AWS::ServiceCatalog::Portfolio` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AServiceCatalog%3A%3APortfolio.properties.json) |
| `AWS::ServiceDiscovery::HttpNamespace` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AServiceDiscovery%3A%3AHttpNamespace.properties.json) |
| `AWS::ServiceDiscovery::Instance` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AServiceDiscovery%3A%3AInstance.properties.json) |
| `AWS::ServiceDiscovery::PublicDnsNamespace` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AServiceDiscovery%3A%3APublicDnsNamespace.properties.json) |
| `AWS::ServiceDiscovery::Service` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AServiceDiscovery%3A%3AService.properties.json) |
| `AWS::Shield::Protection` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AShield%3A%3AProtection.properties.json) |
| `AWS::ShieldRegional::Protection` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AShieldRegional%3A%3AProtection.properties.json) |
| `AWS::Signer::SigningProfile` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ASigner%3A%3ASigningProfile.properties.json) |
| `AWS::StepFunctions::Activity` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AStepFunctions%3A%3AActivity.properties.json) |
| `AWS::StepFunctions::StateMachine` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AStepFunctions%3A%3AStateMachine.properties.json) |
| `AWS::Transfer::Agreement` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ATransfer%3A%3AAgreement.properties.json) |
| `AWS::Transfer::Certificate` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ATransfer%3A%3ACertificate.properties.json) |
| `AWS::Transfer::Connector` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ATransfer%3A%3AConnector.properties.json) |
| `AWS::Transfer::Profile` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ATransfer%3A%3AProfile.properties.json) |
| `AWS::Transfer::Workflow` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3ATransfer%3A%3AWorkflow.properties.json) |
| `AWS::WAF::RateBasedRule` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AWAF%3A%3ARateBasedRule.properties.json) |
| `AWS::WAF::Rule` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AWAF%3A%3ARule.properties.json) |
| `AWS::WAF::RuleGroup` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AWAF%3A%3ARuleGroup.properties.json) |
| `AWS::WAF::WebACL` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AWAF%3A%3AWebACL.properties.json) |
| `AWS::WAFRegional::RateBasedRule` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AWAFRegional%3A%3ARateBasedRule.properties.json) |
| `AWS::WAFRegional::Rule` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AWAFRegional%3A%3ARule.properties.json) |
| `AWS::WAFRegional::RuleGroup` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AWAFRegional%3A%3ARuleGroup.properties.json) |
| `AWS::WAFRegional::WebACL` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AWAFRegional%3A%3AWebACL.properties.json) |
| `AWS::WAFv2::IPSet` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AWAFv2%3A%3AIPSet.properties.json) |
| `AWS::WAFv2::ManagedRuleSet` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AWAFv2%3A%3AManagedRuleSet.properties.json) |
| `AWS::WAFv2::RegexPatternSet` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AWAFv2%3A%3ARegexPatternSet.properties.json) |
| `AWS::WAFv2::RuleGroup` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AWAFv2%3A%3ARuleGroup.properties.json) |
| `AWS::WAFv2::WebACL` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AWAFv2%3A%3AWebACL.properties.json) |
| `AWS::WorkSpaces::ConnectionAlias` | ❌ No | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AWorkSpaces%3A%3AConnectionAlias.properties.json) |
| `AWS::WorkSpaces::Workspace` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AWorkSpaces%3A%3AWorkspace.properties.json) |
| `AWS::XRay::EncryptionConfig` | ✅ Yes | [View Schema](https://github.com/awslabs/aws-config-resource-schema/blob/master/config/properties/resource-types/AWS%3A%3AXRay%3A%3AEncryptionConfig.properties.json) |

## Usage

### Supported Resource Types
For supported resource types, you can:
1. Generate schemas: `python rule-manager.py schema --config your-rule.yaml`
2. Create custom rules using the resource type in your YAML configuration
3. Test rules against real resources: `python rule-manager.py test --config your-rule.yaml`

### Example Rule Configuration
```yaml
rule:
  name: "My-Custom-Rule"
  description: "Custom rule for supported resource type"
  resource_type: "AWS::EC2::Instance"  # Must be from supported list
  platform: "AWS"
  provider: "AWS"
  severity: 1
  logic: |
    package crowdstrike
    default result = "fail"
    result = "pass" if {
        # Your Rego logic here
    }
```

### Regenerate This Table
```bash
python get_schemas.py test-support --provider aws
```

---
*Generated by CrowdStrike Custom IOM Rules Toolkit*
