import jenkins.model.*
import hudson.security.*

def instance = Jenkins.get()

def realm = new HudsonPrivateSecurityRealm(false)
realm.createAccount('user1', 'admin123')
realm.createAccount('user2', 'read123')
instance.setSecurityRealm(realm)

def strategy = new hudson.security.GlobalMatrixAuthorizationStrategy()
// user1: admin
strategy.add(Jenkins.ADMINISTER, 'user1')
// user2: read-only - can log in and view, nothing else
strategy.add(Jenkins.READ, 'user2')
strategy.add(hudson.model.Item.READ, 'user2')
strategy.add(hudson.model.Item.DISCOVER, 'user2')
strategy.add(hudson.model.View.READ, 'user2')
instance.setAuthorizationStrategy(strategy)

instance.save()
println 'security.groovy: users + matrix authorization configured'
